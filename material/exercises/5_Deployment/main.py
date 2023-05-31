import json
import time

import requests


def call():
    """
 curl -X POST http://localhost:8505/v1/models/labelPredictor:predict \
               -H 'Content-type: application/json' \
               -d '{"signature_name": "serving_default", "instances": [{"x": [0, 1, 2]}]}'

      """
    url = 'http://localhost:8505/v1/models/labelPredictor:predict'
    headers = {'Content-type': 'application/json'}
    data = {
        'signature_name': 'serving_default',
        'instances': [{'x': [0]}]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()["predictions"]

def main():
    while True:
        try:
            print(call()[0][0])
        except Exception as e:
            print("Error")
        finally:
            time.sleep(1)


if __name__ == '__main__':
    main()