import json
import time

import requests


def call():
    """
    curl -X POST -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'Content-Length: 37'\
     -H 'Content-type: application/json' -H 'User-Agent: python-requests/2.30.0' \
     -d '{"instances": [[5.1, 3.5, 1.4, 0.2]]}' \
     http://localhost:8501/v1/models/iris:predict
  """
    url = 'http://localhost:8501/v1/models/iris:predict'
    headers = {'Content-type': 'application/json'}
    data = {
        'instances': [[5.1, 3.5, 1.4, 0.2]]
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
