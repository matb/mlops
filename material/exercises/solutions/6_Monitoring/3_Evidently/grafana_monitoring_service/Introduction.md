# Demo

This is an introduction to evidently if used in production.
Will simulate a fast batchprocessing of data which will be sent to a Flask API to be monitored.
The API itself will expose the functionality of evidently and connect it to prometheus.
Finally, we will visualize the results using Grafana

To get started just execute `run_example.py`

- you can then view Grafana using http://localhost:3000 and login with "admin:admin"
- sometimes it happens that you need to login twice
- you find pre-mounted dashboard under Dashboard -> General