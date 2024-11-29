import requests
import json

# Test data
test_data = {
    'customerID': 7000,
    'gender': 1, 
    'SeniorCitizen': 1, 
    'Partner': 1,
    'Dependents': 1,
    'tenure': 2,
    'PhoneService': 20,
    'MultipleLines': 30,
    'InternetService': 13,
    'OnlineSecurity': 22,
    'OnlineBackup': 12,
    'DeviceProtection': 12,
    'TechSupport': 12,
    'StreamingTV': 12,
    'StreamingMovies': 10,
    'Contract': 12,
    'PaperlessBilling': 10,
    'PaymentMethod': 2,
    'MonthlyCharges': 4.85,
    'TotalCharges': 600
}

# Send POST request
response = requests.post(
    "http://localhost:8000/predict",
    json=test_data,
    headers={"Content-Type": "application/json"}
)

# Print results
print("Status Code:", response.status_code)
print("Response:", response.json())
