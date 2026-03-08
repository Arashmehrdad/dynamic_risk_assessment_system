import os
import shutil
import json


with open('config.json', 'r') as f:
    config = json.load(f)

model_path = os.path.join(config['output_model_path'])
prod_deployment_path = os.path.join(config['prod_deployment_path'])
ingested_data_path = os.path.join(config['output_folder_path'])


def store_model_into_pickle():
    """
    Copy the trained model, latest score, and ingested file record
    into the production deployment folder.
    """
    os.makedirs(prod_deployment_path, exist_ok=True)

    shutil.copy(
        os.path.join(model_path, 'trainedmodel.pkl'),
        os.path.join(prod_deployment_path, 'trainedmodel.pkl')
    )

    shutil.copy(
        os.path.join(model_path, 'latestscore.txt'),
        os.path.join(prod_deployment_path, 'latestscore.txt')
    )

    shutil.copy(
        os.path.join(ingested_data_path, 'ingestedfiles.txt'),
        os.path.join(prod_deployment_path, 'ingestedfiles.txt')
    )


if __name__ == '__main__':
    store_model_into_pickle()