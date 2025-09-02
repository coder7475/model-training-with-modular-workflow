## Churn Prediction Pipeline

This project demonstrates a machine learning workflow that provides a structured approach to building, training, and deploying machine learning models.

## Business Context

Aim of this project is to develop a ml system to predict the behavior of customers as to retain customer.

### Table of Contents

- [Dataset](#dataset)
- [Installation](#installation)
- [Directory Structure](#directory-structure)
- [Workflow Steps](#workflow-steps)
- [Contributing](#contributing)
- [License](#license)

### Dataset

The provided dataset can be found at: [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

In this repository: `data-source/Telco-Customer-Churn.csv`

**About Telcom Customer Churn Dataset**

Each row represents a customer, each column contains customer’s attributes described on the column Metadata.

The raw data contains 7043 rows (customers) and 21 columns (features).

The “Churn” column is our target.

### Prerequisites

- python3.8 (or any other version)
- python3.8-venv (venv of that version)

### Installation

To run this project, first install virtual environment:

```bash
python3.8 -m venv venv
```

👉 If `python3.8` is not found, you’ll need to install it first (`sudo apt install python3.8 python3.8-venv` on Ubuntu/Debian).

Then to activate the Python virtual environment, run the following command:

```bash
source venv/bin/activate
```

Check if python version is 3.8:

```
python3 --version
```

If not delete venv folder and try again.

If your python can't be found. Then run the following code to make sure python has path to virtual environments python:

```bash
export PYTHONPATH=~/path_to_directory/model-training-with-modular-workflow
```

Make sure to replace path_to directory with your local path.

To install all packages and initialize the project, run the following command:

```bash
pip install -e .
```

This will run the setup.py file to initialize the project and save metadata.

### Directory Structure

I used this bash script to generate folder structure. If your creating new project to set up the folder structure run the `folder_structure_setup.sh`. Run:

```bash
bash folder_structure_setup.sh
```

This will generate a folder structure necessary for modular workflow. See below:

```bash
├── data-source
├── src
│   ├── __init__.py
│   ├── components
│   │   ├── __init__.py
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   ├── model_monitoring.py
│   │   └── model_trainer.py
│   ├── exception.py
│   ├── logger.py
│   ├── pipelines
│   │   ├── __init__.py
│   │   ├── prediction_pipeline.py
│   │   └── training_pipeline.py
│   └── utils.py
├── .gitignore
├── main.py
├── app.py
├── EDA.ipynb
├── README.md
├── requirements.txt
├── folder_structure_setup.sh
├── test-logging-integration.py
└── test-request.py
```

### Workflow Steps

Machine Learning training and development phase can be divided into 4 steps:

1. **Data Ingestion**: In this step raw data is taken from data sources (e.g database, warehouse etc) and preprocessed and split into training, test and validation sets.

```py
python3 src/components/data_ingestion.py
```

2. **Data transformation**: This is stage for data exploration, data cleaning, feature engineering. It takes raw data from data ingestion stage and creates featured data for model training.

```py
python3 src/components/data_transformation.py
```

3. **Model Training**: This stages takes the featured data from data transformation stage and trains models using the data. This stage work is to select architecture for model continuously train, tune a model. The models is the output of this stage.

Ensure the MLflow server is running before executing:

```bash
python3 src/pipelines/training_pipeline.py
```

4. **Model Evaluation**: This stage compares the trained model to select the best of them. Prepares the model for deployment.

## Tools Used

### 1. **DVC (Data Version Control)**

DVC is used for tracking data files and ensuring version control for datasets.

#### Initialize DVC

```bash
dvc init
```

#### Track Files

```bash
dvc add artifacts/data_ingestion/raw.csv
```

---

### 2. **Feature Store**

The feature store is managed using Feast, allowing storage and retrieval of features.

#### View Feature Store

```bash
cd feature_repo
feast ui
```

---

### 3. **MLflow for Experiment Tracking**

MLflow is used to track experiments and visualize metrics.

#### Start MLflow Server

```bash
mlflow ui
```

You will see mlflow running on `http://127.0.0.1:5000`

---

### 4. **Run ML Pipeline and Experiment Tracking**

Execute the training pipeline and track the experiment metrics on MLflow.

#### Run Training Pipeline

Ensure the MLflow server is running before executing:

```bash
python3 src/pipelines/training_pipeline.py
```

---

### 5. **Run Flask App**

A Flask application is provided for serving the model.

#### Start the Flask App

```bash
python3 app.py
```

---

### 6. **Test the Model API**

Test the API using the provided test file.

#### Run Test Request

```bash
python3 test-flask-app.py
```

#### Expected Output

```bash
Status Code: 200
Response: {'churn_category': 'No', 'prediction': 0, 'status': 'success'}
```

---

## Create API Endpoints with FastAPI

Run flask in dev mode:

1. first change virtual environment to v-fast:

```bash
python3 -m venv v-fast
source v-fast/bin/activate
```

2. Install required packages

```bash
pip install -r fast-requirements.txt
```

3. Run the App in dev mode:

```bash
fastapi dev main.py
```

You will see the app at `https://localhost:8000`

The create api for ml model inference is `https://localhost:8000/predict`

# Deploy to production

Use docker to build a image to deploy:

```bash
docker build -t flask-ml:0 .
```

Run the container in detach mode to deploy:

```bash
docker run -d -p 8000:8000 flask-ml:0
```
