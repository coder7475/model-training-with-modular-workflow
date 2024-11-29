# Predict route
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.pipelines.prediction_pipeline import PredictionPipeline
from src.pipelines.prediction_pipeline import CustomClass

app = FastAPI()

# Root Route
@app.get("/")
async def index():
    return {"message": "Hello, FastAPI!"}

# Predict Route
@app.post("/predict")
async def predict(payload: CustomClass):
    try:
        # Create CustomClass instance with the payload data
        data = CustomClass(
            customerID=payload.customerID,
            gender=payload.gender,
            SeniorCitizen=payload.SeniorCitizen,
            Partner=payload.Partner,
            Dependents=payload.Dependents,
            tenure=payload.tenure,
            PhoneService=payload.PhoneService,
            MultipleLines=payload.MultipleLines,
            InternetService=payload.InternetService,
            OnlineSecurity=payload.OnlineSecurity,
            OnlineBackup=payload.OnlineBackup,
            DeviceProtection=payload.DeviceProtection,
            TechSupport=payload.TechSupport,
            StreamingTV=payload.StreamingTV,
            StreamingMovies=payload.StreamingMovies,
            Contract=payload.Contract,
            PaperlessBilling=payload.PaperlessBilling,
            PaymentMethod=payload.PaymentMethod,
            MonthlyCharges=payload.MonthlyCharges,
            TotalCharges=payload.TotalCharges
        )

        # Get the DataFrame from the CustomClass instance
        final_data = data.get_data_DataFrame()

        # Predict using the pipeline
        pipeline_prediction = PredictionPipeline()
        pred = pipeline_prediction.predict(final_data)

        # Return the prediction result
        return {
            "status": "success",
            "prediction": int(pred[0]),
            "churn_category": "No" if pred[0] == 0 else "Yes"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
