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

test_data_2 = {
    'customerID': 557543,
    'gender': 1, 
    'SeniorCitizen': 1, 
    'Partner': 1,
    'Dependents': 1,
    'tenure': 34,
    'PhoneService': 1,
    'MultipleLines': 1,
    'InternetService': 1,
    'OnlineSecurity': 2,
    'OnlineBackup': 1,
    'DeviceProtection': 2,
    'TechSupport': 1,
    'StreamingTV': 1,
    'StreamingMovies': 1,
    'Contract': 1,
    'PaperlessBilling': 1,
    'PaymentMethod': 1,
    'MonthlyCharges': 563.95,
    'TotalCharges': 188329.5
}

# Send POST request 1
response = requests.post(
    "http://localhost:8000/predict",
    json=test_data,
    headers={"Content-Type": "application/json"}
)

# Print results
print("Status Code:", response.status_code)
print("Response:", response.json())

# Send POST request 2
response = requests.post(
    "http://localhost:8000/predict",
    json=test_data_2,
    headers={"Content-Type": "application/json"}
)

# Print results
print("Status Code:", response.status_code)
print("Response:", response.json())

