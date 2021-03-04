import os
import json

import pandas as pd

from utils import (
    normalize_features,
    get_pickle
)

def response(body={}, status_code=200):
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
    }

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', ''))
        pkl = get_pickle('pickles/factory_linear_regression.pkl')

        df = pd.DataFrame([body])
        X = df[['temp', 'vibration', 'current', 'noise']]
        X = normalize_features(X)

        prediction = pkl['model'].predict(X)
        encoding_prediction = pkl['encoding'][prediction[0]]
    except Exception as e:
        return response({ "Error": str(e) }, 500)
    else:
        return response({ "prediction": encoding_prediction }, 200)

