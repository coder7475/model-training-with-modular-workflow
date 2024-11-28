## ML Modular Workflow Setup

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
python3 -m venv venv
```

Then to activate the Python virtual environment, run the following command:

```bash
source venv/bin/activate
```

Then run the following code to make sure python has path to virtual environments python:

```bash
export PYTHONPATH=~/path_to_directory/model-training-with-modular-workflow
```

Make sure to replace path_to directory with your local path.

To install all packages and initialize the project, run the following command:

```bash
pip install -e .
```

This will run the setup.py file to initialize the project and save metadata. Make sure you have `requirements.txt`,
`README.md` file ready.

### Directory Structure

To set up the folder structure run the `folder_structure_setup.sh`. Run:

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

2. **Data transformation**: This is stage for data exploration, data cleaning, feature engineering. It takes raw data from data ingestion stage and creates featured data for model training.

3. **Model Training**: This stages takes the featured data from data transformation stage and trains models using the data. This stage work is to select architecture for model continuously train, tune a model. The models is the output of this stage.

4. **Model Evaluation**: This stage compares the trained model to select the best of them. Prepares the model for deployment.

The deployment and monitoring phase for ML model includes:

1. **Backend App Development**: Create a backend app to serve the model through api.
2. **Testing**: Testing the app serves correctly.
3. **Monitoring**: Monitoring the app is healthy and can serve reliably.

### Tools Used

1. **DVC (Data Version Control)**

DVC

```bash
dvc init
```

Track using

```bash
dvc add artifacts/data_ingestion/raw.csv
```

### Feature Store

To see the features in feature store

```bash
cd feature_repo
feast ui
```

### Run MLFLOW For expeirement tracking

Run mlflow

```bash
mlflow ui
```

### Run ml pipeline and experiment tracking

Keep the mlflow server running then simply run:

```bash
python3 src/pipelines/training_pipeline.py
```

### Run flask app

```bash
python3 app.py
```

### Test with a test file

```bash
python3 test-request.py
```

Output:

```bash
Status Code: 200
Response: {'churn_category': 'No', 'prediction': 0, 'status': 'success'}
```

## Fast API

Dev mode

```bash
fastapi dev main.py
```

Production mode

```bash
fastapi run main.py
```
