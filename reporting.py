import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import diagnostics


with open('config.json', 'r') as f:
    config = json.load(f)

test_data_path = os.path.join(config['test_data_path'])
output_model_path = os.path.join(config['output_model_path'])


def score_model():
    """
    Generate and save a confusion matrix plot using the deployed model
    predictions on the test dataset.
    """
    test_data = pd.read_csv(os.path.join(test_data_path, 'testdata.csv'))

    y_true = test_data['exited']
    y_pred = diagnostics.model_predictions(test_data)

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()

    plt.savefig(os.path.join(output_model_path, 'confusionmatrix.png'))
    plt.close()


if __name__ == '__main__':
    score_model()