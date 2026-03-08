from flask import Flask, jsonify, request
import pandas as pd
import os
import json

import diagnostics
import scoring


app = Flask(__name__)

with open('config.json', 'r') as f:
    config = json.load(f)

test_data_path = os.path.join(config['test_data_path'])


@app.route('/prediction', methods=['POST', 'OPTIONS'])
def predict():
    """
    Return model predictions for a dataset path provided in the request.
    """
    if request.method == 'OPTIONS':
        return '', 200

    data_path = request.args.get('filename')

    test_data = pd.read_csv(data_path)
    predictions = diagnostics.model_predictions(test_data)
    predictions = [int(x) for x in predictions]

    return jsonify({'predictions': predictions}), 200


@app.route('/scoring', methods=['GET', 'OPTIONS'])
def score():
    """
    Return the latest F1 score.
    """
    if request.method == 'OPTIONS':
        return '', 200

    score_value = scoring.score_model()

    return jsonify({'f1_score': score_value}), 200


@app.route('/summarystats', methods=['GET', 'OPTIONS'])
def stats():
    """
    Return summary statistics for the ingested dataset.
    """
    if request.method == 'OPTIONS':
        return '', 200

    summary = diagnostics.dataframe_summary()

    return jsonify({'summary_statistics': summary}), 200


@app.route('/diagnostics', methods=['GET', 'OPTIONS'])
def diagnostic():
    """
    Return timing, missing data, and outdated package information.
    """
    if request.method == 'OPTIONS':
        return '', 200

    timings = diagnostics.execution_time()
    missing = diagnostics.missing_data()
    packages = diagnostics.outdated_packages_list()

    return jsonify({
        'execution_time': timings,
        'missing_data_percentages': missing,
        'outdated_packages': packages
    }), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)