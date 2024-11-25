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
