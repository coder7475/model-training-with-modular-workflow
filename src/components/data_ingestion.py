import os, sys
import pandas as pd
import numpy as np
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionConfig:
    train_data_path = os.path.join("artifacts/data_ingestion", "train.csv")
    test_data_path = os.path.join("artifacts/data_ingestion", "test.csv")
    raw_data_path = os.path.join("artifacts/data_ingestion", "raw.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logging.info("Data Ingestion has been started")
        try: 
            logging.info("Data reading using Pandas from local file system")
            data = pd.read_csv(os.path.join("data-source", "cleaned_data.csv"))
            logging.info("Data Reading has been completed")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info("Raw data has been stored")

            train_set, test_set = train_test_split(data, test_size= .20, random_state=42)
            logging.info("Raw data has been splitted into Train and Test set")

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Data Ingestion has been completed!")
            
            return self.ingestion_config.train_data_path, self.ingestion_config.test_data_path 
        except Exception as e:
            logging.info("Error occured in data ingestion stage")
            raise CustomException(e, sys)

