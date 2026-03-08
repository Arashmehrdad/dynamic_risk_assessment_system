import os
import json
import pickle
import timeit
import subprocess
import pandas as pd


with open('config.json', 'r') as f:
    config = json.load(f)

output_folder_path = os.path.join(config['output_folder_path'])
prod_deployment_path = os.path.join(config['prod_deployment_path'])


def model_predictions(test_data):
    """
    Read the deployed model and return predictions for the input dataframe.
    """
    with open(os.path.join(prod_deployment_path, 'trainedmodel.pkl'), 'rb') as f:
        model = pickle.load(f)

    X = test_data[['lastmonth_activity', 'lastyear_activity', 'number_of_employees']]
    predictions = model.predict(X)

    return list(predictions)


def dataframe_summary():
    """
    Calculate mean, median, and standard deviation for numeric columns.
    """
    df = pd.read_csv(os.path.join(output_folder_path, 'finaldata.csv'))
    numeric_df = df[['lastmonth_activity', 'lastyear_activity', 'number_of_employees']]

    means = list(numeric_df.mean())
    medians = list(numeric_df.median())
    stds = list(numeric_df.std())

    return [means, medians, stds]


def missing_data():
    """
    Calculate the percentage of missing values in each column.
    """
    df = pd.read_csv(os.path.join(output_folder_path, 'finaldata.csv'))
    missing_percentages = list(df.isna().sum() / len(df))

    return missing_percentages


def execution_time():
    """
    Time ingestion.py and training.py in seconds.
    """
    ingestion_time = timeit.timeit('import ingestion; ingestion.merge_multiple_dataframe()', number=1)
    training_time = timeit.timeit('import training; training.train_model()', number=1)

    return [ingestion_time, training_time]


def outdated_packages_list():
    """
    Return package version information using pip.
    """
    result = subprocess.run(
        ['python', '-m', 'pip', 'list', '--outdated'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return result.stdout


if __name__ == '__main__':
    print('Model predictions function and diagnostics loaded.')