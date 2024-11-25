## ml-workflow-template

This project is a machine learning workflow template that provides a structured approach to building, training, and deploying machine learning models.

### Table of Contents

- [Installation](#installation)
- [Directory Structure](#directory-structure)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

### Installation

To set up the project, clone the repository and run the `folder_structure_setup.sh` script to create the necessary directories and files.

To install virtual environment:

```bash
python3 -m venv venv
```

To activate the Python virtual environment, navigate to the project directory in your terminal and run the following command:

```bash
source venv/bin/activate
export PYTHONPATH=~/path_to_directory/model-training-with-modular-workflow
```

To install all packages from requirements.txt, run the following command:

```bash
pip install -e .
```

### Directory Structure

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

### Usage

### Data Version Control

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
