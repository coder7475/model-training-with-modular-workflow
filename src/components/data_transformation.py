import os
import sys
import pandas as pd
import numpy as np
from src.logger import logging
from src.exception import CustomException
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from dataclasses import dataclass
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from src.utils import save_object
# Feast
from feast import Field, FeatureStore, Entity, FeatureView, FileSource
from feast.types import Int64, String, Float64
from feast.value_type import ValueType
from datetime import datetime, timedelta

@dataclass
class DataTransformationConfig:
    preprocess_obj_file_path = os.path.join("artifacts/data_transformation", "preprocessor.pkl")
    feature_store_repo_path = "feature_repo"

class DataTransformation:
    def __init__(self):
        try:
            self.data_transformation_config = DataTransformationConfig()
            
            # Get absolute path and create directory structure
            repo_path = os.path.abspath(self.data_transformation_config.feature_store_repo_path)
            os.makedirs(os.path.join(repo_path, "data"), exist_ok=True)
            
            # Create feature store yaml with minimal configuration
            feature_store_yaml_path = os.path.join(repo_path, "feature_store.yaml")
            
            # Simplified, minimal feature store configuration
            feature_store_yaml = """project: churn_prediction
provider: local
registry: data/registry.db
online_store:
  type: sqlite
offline_store:
  type: file
entity_key_serialization_version: 2"""
            
            # Write configuration file
            with open(feature_store_yaml_path, 'w') as f:
                f.write(feature_store_yaml)
            
            logging.info(f"Created feature store configuration at {feature_store_yaml_path}")
            
            # Initialize feature store
            self.feature_store = FeatureStore(repo_path=repo_path)
            logging.info("Feature store initialized successfully")

        except Exception as e:
            logging.error(f"Error in initialization: {str(e)}")
            raise CustomException(e, sys)

    def get_data_transformation_obj(self):
        try:
            logging.info("Data Transformation Started")
          
            numerical_features = [
                     "gender", "SeniorCitizen", "Partner", "Dependents", "tenure", 
                    "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
                    "DeviceProtection","TechSupport","StreamingTV","StreamingMovies","Contract",
                    "PaperlessBilling","PaymentMethod","MonthlyCharges","TotalCharges"
            ]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy='median')),
                    ("scaler", StandardScaler())
                ]
            )

            preprocessor = ColumnTransformer([
                ("num_pipeline", num_pipeline, numerical_features)
            ])

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def remove_outliers_IQR(self, col, df):
        try:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            upper_limit = Q3 + 1.5 * IQR
            lower_limit = Q1 - 1.5 * IQR
            
            df.loc[(df[col] > upper_limit), col] = upper_limit
            df.loc[(df[col] < lower_limit), col] = lower_limit
            
            return df

        except Exception as e:
            logging.info("Outliers handling code")
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformation_obj()

            target_column_name = 'Churn'

            input_feature_train_df = train_data.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_data[target_column_name]

            input_feature_test_df = test_data.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_data[target_column_name]

            logging.info("Applying preprocessing object on training and testing datasets.")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            logging.info("Starting feature store operations")
            
            # Push data to Feast feature store
            self.push_features_to_store(train_data, "train")
            logging.info("Pushed training data to feature store")
            
            self.push_features_to_store(test_data, "test")
            logging.info("Pushed testing data to feature store")

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_transformation_config.preprocess_obj_file_path,
                obj=preprocessing_obj
            )

            return train_arr, test_arr, self.data_transformation_config.preprocess_obj_file_path

        except Exception as e:
            logging.error(f"Error in data transformation: {str(e)}")
            raise CustomException(e, sys)

    def push_features_to_store(self, df, entity_id):
        try:
            # Create a copy to avoid modifying the original dataframe
            df_copy = df.copy()
            
            # Clean and validate the data before saving
            logging.info(f"Original dataframe shape: {df_copy.shape}")
            logging.info(f"Original dataframe columns: {df_copy.columns.tolist()}")
            
            # Handle missing values in TotalCharges (convert to numeric)
            if 'TotalCharges' in df_copy.columns:
                df_copy['TotalCharges'] = pd.to_numeric(df_copy['TotalCharges'], errors='coerce')
                df_copy['TotalCharges'] = df_copy['TotalCharges'].fillna(0.0)
            
            # Add timestamp column if not present
            if 'event_timestamp' not in df_copy.columns:
                df_copy['event_timestamp'] = pd.Timestamp.now()
            
            # Add entity_id column if not present
            if 'entity_id' not in df_copy.columns:
                df_copy['entity_id'] = range(len(df_copy))
            
            # Convert data types to ensure compatibility
            df_copy['entity_id'] = df_copy['entity_id'].astype('int64')
            
            # Ensure timestamp is datetime
            df_copy['event_timestamp'] = pd.to_datetime(df_copy['event_timestamp'])

            # Save data as parquet
            data_path = os.path.join(
                self.data_transformation_config.feature_store_repo_path,
                "data"
            )
            parquet_path = os.path.join(data_path, f"{entity_id}_features.parquet")
            
            # Ensure the directory exists
            os.makedirs(data_path, exist_ok=True)
            
            # Save the parquet file with specific settings
            df_copy.to_parquet(parquet_path, index=False, engine='pyarrow')
            logging.info(f"Saved feature data to {parquet_path}")
            
            # Verify the parquet file was created and can be read
            try:
                test_df = pd.read_parquet(parquet_path)
                logging.info(f"Verified parquet file. Shape: {test_df.shape}")
            except Exception as read_error:
                logging.error(f"Failed to read back parquet file: {read_error}")
                raise

            # Define data source with relative path
            data_source = FileSource(
                path=f"data/{entity_id}_features.parquet",
                timestamp_field="event_timestamp"
            )

            # Define entity
            entity = Entity(
                name="entity_id",
                value_type=ValueType.INT64,
                description="Entity ID"
            )

            # Define feature view with proper field definitions
            feature_fields = [
                Field(name="customerID", dtype=String),  
                Field(name="gender", dtype=String),
                Field(name="SeniorCitizen", dtype=Int64),
                Field(name="Partner", dtype=String),
                Field(name="Dependents", dtype=String),
                Field(name="tenure", dtype=Int64),
                Field(name="PhoneService", dtype=String),
                Field(name="MultipleLines", dtype=String),
                Field(name="InternetService", dtype=String),
                Field(name="OnlineSecurity", dtype=String),
                Field(name="OnlineBackup", dtype=String),
                Field(name="DeviceProtection", dtype=String),
                Field(name="TechSupport", dtype=String),
                Field(name="StreamingTV", dtype=String),
                Field(name="StreamingMovies", dtype=String),
                Field(name="Contract", dtype=String),
                Field(name="PaperlessBilling", dtype=String),
                Field(name="PaymentMethod", dtype=String),
                Field(name="MonthlyCharges", dtype=Float64),  
                Field(name="TotalCharges", dtype=Float64)  # Changed from String to Float64
            ]
            
            # Only include fields that exist in the dataframe
            existing_fields = []
            for field in feature_fields:
                if field.name in df_copy.columns:
                    existing_fields.append(field)
                else:
                    logging.warning(f"Field {field.name} not found in dataframe columns")
            
            logging.info(f"Including {len(existing_fields)} fields in feature view")

            feature_view = FeatureView(
                name=f"{entity_id}_features",
                entities=[entity],               
                schema=existing_fields,
                source=data_source,
                online=True,
                ttl=timedelta(days=365)  # Add TTL to prevent data expiry issues
            )

            # Apply to feature store with error handling
            try:
                self.feature_store.apply([entity, feature_view])
                logging.info(f"Applied entity and feature view for {entity_id}")
            except Exception as apply_error:
                logging.error(f"Failed to apply entity/feature view: {apply_error}")
                # Continue without raising to allow basic transformation to complete
                return

            # Materialize features with error handling
            try:
                self.feature_store.materialize(
                    start_date=datetime.now() - timedelta(days=2),
                    end_date=datetime.now() + timedelta(days=1)
                )
                logging.info("Materialized features successfully")
            except Exception as materialize_error:
                logging.error(f"Failed to materialize features: {materialize_error}")
                # Continue without raising to allow basic transformation to complete
                return

        except Exception as e:
            logging.error(f"Error in push_features_to_store: {str(e)}")
            # Don't raise the exception to allow basic data transformation to complete
            logging.warning("Continuing with basic data transformation without feature store")

    def retrieve_features_from_store(self, entity_id, num_entities):
        try:
            feature_refs = [                  
                f"{entity_id}_features:gender",
                f"{entity_id}_features:SeniorCitizen",
                f"{entity_id}_features:Partner",
                f"{entity_id}_features:Dependents",
                f"{entity_id}_features:tenure",
                f"{entity_id}_features:PhoneService",
                f"{entity_id}_features:MultipleLines",
                f"{entity_id}_features:InternetService",
                f"{entity_id}_features:OnlineSecurity",
                f"{entity_id}_features:OnlineBackup",
                f"{entity_id}_features:DeviceProtection",
                f"{entity_id}_features:TechSupport",
                f"{entity_id}_features:StreamingTV",
                f"{entity_id}_features:StreamingMovies",
                f"{entity_id}_features:Contract",
                f"{entity_id}_features:PaperlessBilling",
                f"{entity_id}_features:PaymentMethod",
                f"{entity_id}_features:MonthlyCharges",
                f"{entity_id}_features:TotalCharges"
            ]
            
            entity_rows = [{"entity_id": i} for i in range(num_entities)]
            
            feature_vector = self.feature_store.get_online_features(                
                feature_refs=feature_refs,
                entity_rows=entity_rows
            ).to_df()

            logging.info(f"Retrieved features for {entity_id}")
            return feature_vector

        except Exception as e:
            logging.error(f"Error in retrieve_features_from_store: {str(e)}")
            raise CustomException(e, sys)
        

# Add main to run the data transformation
if __name__ == "__main__":
    try:
        # You may need to adjust these paths as per your data ingestion config
        train_path = os.path.join("artifacts/data_ingestion", "train.csv")
        test_path = os.path.join("artifacts/data_ingestion", "test.csv")
        
        # Check if files exist
        if not os.path.exists(train_path):
            raise FileNotFoundError(f"Training data not found at {train_path}")
        if not os.path.exists(test_path):
            raise FileNotFoundError(f"Testing data not found at {test_path}")
            
        logging.info("Starting Data Transformation main execution")
        transformer = DataTransformation()
        train_arr, test_arr, preprocessor_path = transformer.initiate_data_transformation(train_path, test_path)
        print(f"Data transformation completed.\nTrain array shape: {train_arr.shape}\nTest array shape: {test_arr.shape}")
        print(f"Preprocessor object saved at: {preprocessor_path}")
    except Exception as e:
        print(f"Error running data transformation: {e}")
        import traceback
        traceback.print_exc()