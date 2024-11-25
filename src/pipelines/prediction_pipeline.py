import os, sys
from src.logger import logging
from src.exception import CustomException
import numpy as np
import pandas as pd
from dataclasses import dataclass
from src.utils import load_object

@dataclass
class PredictionPipeline:
    def predict(self, features):
        preprocessor_path = os.path.join("artifacts/data_transformation", "preprocessor.pkl")
        model_path = os.path.join("artifacts/model_trainer", "model.pkl")

        processor = load_object(preprocessor_path)
        model = load_object(model_path)

        scaled = processor.transform(features)
        pred = model.predict(scaled)

        return pred


@dataclass
class CustomClass:
    customerID: str
    gender: int
    SeniorCitizen: int
    Partner: int
    Dependents: int
    tenure: int
    PhoneService: int
    MultipleLines: int
    InternetService: int
    OnlineSecurity: int
    OnlineBackup: int
    DeviceProtection: int
    TechSupport: int
    StreamingTV: int
    StreamingMovies: int
    Contract: int
    PaperlessBilling: int
    PaymentMethod: int
    MonthlyCharges: float
    TotalCharges: float

    def get_data_DataFrame(self):
        try:
            data_dict = self.__dict__
            data = pd.DataFrame([data_dict])
            return data
        except Exception as e:
            raise CustomException(e, sys)






