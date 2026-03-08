import pandas as pd
import pickle
import os
from sklearn.metrics import f1_score
import json


with open('config.json', 'r') as f:
    config = json.load(f)

test_data_path = os.path.join(config['test_data_path'])
model_path = os.path.join(config['output_model_path'])


def score_model():
    """
    Score the trained model on the test dataset using F1 score
    and save the result to latestscore.txt.
    """
    test_data = pd.read_csv(os.path.join(test_data_path, 'testdata.csv'))

    X_test = test_data[['lastmonth_activity', 'lastyear_activity', 'number_of_employees']]
    y_test = test_data['exited']

    with open(os.path.join(model_path, 'trainedmodel.pkl'), 'rb') as f:
        model = pickle.load(f)

    predictions = model.predict(X_test)
    score = f1_score(y_test, predictions)

    with open(os.path.join(model_path, 'latestscore.txt'), 'w') as f:
        f.write(str(score))

    return score


if __name__ == '__main__':
    score_model()