import requests
import json

# Test data
test_data = {
    'customerID': 7000,
    'gender': 1, 
    'SeniorCitizen': 1, 
    'Partner': 0,
    'Dependents': 1,
    'tenure': 0,
    'PhoneService': 0,
    'MultipleLines': 0,
    'InternetService': 1,
    'OnlineSecurity': 2,
    'OnlineBackup': 1,
    'DeviceProtection': 1,
    'TechSupport': 1,
    'StreamingTV': 1,
    'StreamingMovies': 0,
    'Contract': 1,
    'PaperlessBilling': 0,
    'PaymentMethod': 29.85,
    'MonthlyCharges': 29.85,
    'TotalCharges': 200
}

# Send POST request
response = requests.post(
    "http://localhost:5000/predict",
    json=test_data,
    headers={"Content-Type": "application/json"}
)

# Print results
print("Status Code:", response.status_code)
print("Response:", response.json())
