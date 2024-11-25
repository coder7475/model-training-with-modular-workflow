from flask import Flask, request, jsonify
from src.pipelines.prediction_pipeline import PredictionPipeline
from src.pipelines.prediction_pipeline import CustomClass 

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from the request
        json_data = request.get_json()

        # Create CustomClass instance with JSON data
        data = CustomClass(
            customerID=json_data.get("customerID"),
            gender=int(json_data.get("gender")),
            SeniorCitizen=int(json_data.get("SeniorCitizen")),
            Partner=int(json_data.get("Partner")),
            Dependents=int(json_data.get("Dependents")),
            tenure=int(json_data.get("tenure")),
            PhoneService=int(json_data.get("PhoneService")),
            MultipleLines=int(json_data.get("MultipleLines")),
            InternetService=int(json_data.get("InternetService")),
            OnlineSecurity=int(json_data.get("OnlineSecurity")),
            OnlineBackup=int(json_data.get("OnlineBackup")),
            DeviceProtection=int(json_data.get("DeviceProtection")),
            TechSupport=int(json_data.get("TechSupport")),
            StreamingTV=int(json_data.get("StreamingTV")),
            StreamingMovies=int(json_data.get("StreamingMovies")),
            Contract=int(json_data.get("Contract")),
            PaperlessBilling=int(json_data.get("PaperlessBilling")),
            PaymentMethod=int(json_data.get("PaymentMethod")),
            MonthlyCharges=float(json_data.get("MonthlyCharges")),
            TotalCharges=float(json_data.get("TotalCharges"))
        )

        # Get the DataFrame from the CustomClass instance
        final_data = data.get_data_DataFrame()

        # Predict using the pipeline
        pipeline_prediction = PredictionPipeline()
        pred = pipeline_prediction.predict(final_data)

        # Return the prediction result
        return jsonify({
            "status": "success",
            "prediction": int(pred[0]),
            "churn_category": "No" if pred[0] == 0 else "Yes"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
