import os
import json
import urllib.request
import urllib.parse


with open('config.json', 'r') as f:
    config = json.load(f)

output_model_path = os.path.join(config['output_model_path'])


def read_url(url, method='GET'):
    """
    Send an HTTP request and return the decoded response text.
    """
    req = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')


def api_calls():
    """
    Call all API endpoints and save their combined outputs to apireturns.txt.
    """
    prediction_params = urllib.parse.urlencode({'filename': 'testdata/testdata.csv'})
    prediction_url = 'http://127.0.0.1:8000/prediction?' + prediction_params

    response1 = read_url(prediction_url, method='POST')
    response2 = read_url('http://127.0.0.1:8000/scoring')
    response3 = read_url('http://127.0.0.1:8000/summarystats')
    response4 = read_url('http://127.0.0.1:8000/diagnostics')

    responses = (
        'Prediction Endpoint Output:\n' + response1 + '\n\n' +
        'Scoring Endpoint Output:\n' + response2 + '\n\n' +
        'Summary Statistics Endpoint Output:\n' + response3 + '\n\n' +
        'Diagnostics Endpoint Output:\n' + response4
    )

    with open(os.path.join(output_model_path, 'apireturns.txt'), 'w') as f:
        f.write(responses)


if __name__ == '__main__':
    api_calls()