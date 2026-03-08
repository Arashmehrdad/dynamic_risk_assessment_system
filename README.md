# Dynamic Risk Assessment System

This project implements a dynamic risk assessment system for corporate client attrition. The goal is to predict which clients are at risk of terminating their contracts, deploy the model, monitor performance, and automatically retrain and redeploy the model when needed.

## Project Overview

The system was built as part of the Udacity Machine Learning DevOps project. It includes:

* Automated data ingestion
* Model training and scoring
* Model deployment
* Diagnostics and monitoring
* Reporting
* API endpoints for predictions and diagnostics
* Full process automation with cron

The model predicts client attrition risk based on historical activity and employee-related features.

## Project Structure

```text
.
|-- apicalls.py
|-- app.py
|-- config.json
|-- cronjob.txt
|-- deployment.py
|-- diagnostics.py
|-- fullprocess.py
|-- ingestion.py
|-- reporting.py
|-- scoring.py
|-- training.py
|-- wsgi.py
|-- practicedata/
|   |-- dataset1.csv
|   |-- dataset2.csv
|-- sourcedata/
|   |-- dataset3.csv
|   |-- dataset4.csv
|-- testdata/
|   |-- testdata.csv
|-- ingesteddata/
|   |-- finaldata.csv
|   |-- ingestedfiles.txt
|-- practicemodels/
|   |-- trainedmodel.pkl
|   |-- latestscore.txt
|   |-- confusionmatrix.png
|   |-- apireturns.txt
|-- models/
|   |-- trainedmodel.pkl
|   |-- latestscore.txt
|   |-- confusionmatrix.png
|   |-- confusionmatrix2.png
|   |-- apireturns.txt
|   |-- apireturns2.txt
|-- production_deployment/
|   |-- trainedmodel.pkl
|   |-- latestscore.txt
|   |-- ingestedfiles.txt
```

## Dataset Description

The datasets contain fabricated information about hypothetical corporations. Each row represents one corporate client.

### Features

* `corporation`: corporation identifier
* `lastmonth_activity`: activity level in the previous month
* `lastyear_activity`: activity level in the previous year
* `number_of_employees`: number of employees in the corporation
* `exited`: target variable where:

  * `1` = client exited
  * `0` = client remained

## Project Steps

### 1. Data Ingestion

`ingestion.py`:

* Reads all CSV files from the input folder
* Merges them into one dataset
* Removes duplicate rows
* Saves the result as `finaldata.csv`
* Saves a record of ingested filenames in `ingestedfiles.txt`

### 2. Training, Scoring, and Deployment

* `training.py` trains a logistic regression model
* `scoring.py` calculates the F1 score on test data
* `deployment.py` copies the model, score, and ingestion record to the production deployment folder

### 3. Diagnostics

`diagnostics.py` provides:

* model predictions using the deployed model
* summary statistics
* missing data percentages
* execution time for ingestion and training
* outdated package checks

### 4. Reporting

* `reporting.py` generates a confusion matrix plot
* `app.py` provides API endpoints
* `apicalls.py` calls all endpoints and writes outputs to `apireturns.txt`

### 5. Process Automation

`fullprocess.py`:

* checks for new data
* checks for model drift
* retrains and redeploys the model if needed
* regenerates reports and API outputs

A cron job is included in `cronjob.txt` to run the full process every 10 minutes.

## How to Run

### 1. Data ingestion

```bash
python ingestion.py
```

### 2. Train the model

```bash
python training.py
```

### 3. Score the model

```bash
python scoring.py
```

### 4. Deploy the model

```bash
python deployment.py
```

### 5. Run diagnostics

You can test individual diagnostic functions with Python, for example:

```bash
python -c "import diagnostics; print(diagnostics.dataframe_summary())"
```

### 6. Generate reporting output

```bash
python reporting.py
```

### 7. Start the API

```bash
python app.py
```

### 8. Call all API endpoints

With the Flask app running:

```bash
python apicalls.py
```

### 9. Run the full automated pipeline

```bash
python fullprocess.py
```

## API Endpoints

The Flask app exposes the following endpoints:

### `/prediction`

Returns predictions for a provided dataset path.

Example:

```bash
curl -X POST "http://127.0.0.1:8000/prediction?filename=testdata/testdata.csv"
```

### `/scoring`

Returns the latest F1 score.

Example:

```bash
curl "http://127.0.0.1:8000/scoring"
```

### `/summarystats`

Returns summary statistics for the ingested dataset.

Example:

```bash
curl "http://127.0.0.1:8000/summarystats"
```

### `/diagnostics`

Returns:

* execution time
* missing data percentages
* outdated package information

Example:

```bash
curl "http://127.0.0.1:8000/diagnostics"
```

## Automation

The cron job used for automation is:

```text
*/10 * * * * cd /home/workspace && /root/miniconda3/envs/mldevops-c4/bin/python fullprocess.py
```

This runs the full monitoring and redeployment pipeline every 10 minutes.

## Model

The project uses a **Logistic Regression** model from scikit-learn for binary classification of attrition risk.

## Outputs

Important generated outputs include:

* `ingesteddata/finaldata.csv`
* `ingesteddata/ingestedfiles.txt`
* `practicemodels/trainedmodel.pkl`
* `practicemodels/latestscore.txt`
* `models/confusionmatrix.png`
* `models/confusionmatrix2.png`
* `models/apireturns.txt`
* `models/apireturns2.txt`
* `production_deployment/trainedmodel.pkl`
* `production_deployment/latestscore.txt`
* `production_deployment/ingestedfiles.txt`

## Notes

* Practice data is used in the early project steps.
* Production-style automation uses `sourcedata` and `models` through the final `config.json`.
* The project was developed in the Udacity workspace environment.

## Author

Arash Mehrdad
