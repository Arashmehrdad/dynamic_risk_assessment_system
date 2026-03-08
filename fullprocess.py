import os
import json
import shutil
import pandas as pd

import ingestion
import training
import scoring
import deployment
import diagnostics
import reporting
import apicalls


with open('config.json', 'r') as f:
    config = json.load(f)

input_folder_path = os.path.join(config['input_folder_path'])
output_folder_path = os.path.join(config['output_folder_path'])
prod_deployment_path = os.path.join(config['prod_deployment_path'])


def read_ingested_files():
    """
    Read previously ingested filenames from production deployment.
    """
    ingested_file_path = os.path.join(prod_deployment_path, 'ingestedfiles.txt')

    if not os.path.exists(ingested_file_path):
        return []

    with open(ingested_file_path, 'r') as f:
        content = f.read().strip()

    if not content:
        return []

    return eval(content)


def check_new_files():
    """
    Check whether there are new source files not yet ingested.
    """
    current_files = [file for file in os.listdir(input_folder_path) if file.endswith('.csv')]
    ingested_files = read_ingested_files()

    new_files = [file for file in current_files if file not in ingested_files]
    return new_files


def model_drift_detected():
    """
    Check whether the newly scored model is worse than the deployed one.
    If no new model exists yet in the models folder, treat it as drift.
    """
    latest_score_path = os.path.join(prod_deployment_path, 'latestscore.txt')
    new_model_score_path = os.path.join(config['output_model_path'], 'latestscore.txt')
    new_model_file_path = os.path.join(config['output_model_path'], 'trainedmodel.pkl')

    if not os.path.exists(latest_score_path):
        return True

    if not os.path.exists(new_model_file_path):
        return True

    with open(latest_score_path, 'r') as f:
        deployed_score = float(f.read().strip())

    new_score = scoring.score_model()

    return new_score < deployed_score


def run_full_process():
    """
    Run the full pipeline only if there is new data and model drift.
    """
    new_files = check_new_files()

    if len(new_files) == 0:
        print('No new data found. Process ended.')
        return

    ingestion.merge_multiple_dataframe()

    if not model_drift_detected():
        print('No model drift detected. Process ended.')
        return

    training.train_model()
    scoring.score_model()
    deployment.store_model_into_pickle()
    reporting.score_model()
    apicalls.api_calls()

    print('Full process completed.')


if __name__ == '__main__':
    run_full_process()