# Instructions

Sometimes it can happen that the basic metrics exposed are not enough and you want to monitor more business related KPI.
This can also be achieved leveraging prometheus and the python client for it.

- Here we have provided you an example of a simple machinelearning model and a API with a few nice-to-haves for
  production.
- You can take a look into the app.py and see that we have implemented a few addition endpoints that a production api
  need:
    - A healthcheck
    - A UUID-Middleware to uniquely identify requests
    - Some middlewares to expose our own statistics for prometheus.
- Now have a look into our middleware.py
    - In this file we define two metrics for prometheus
    - first a Counter that counts the requests - similar to the one earlier in our TF Serving
    - the second one is a Summary that is able to log single events - e.g. success, response time or response size.

## Task

Please now go ahead and create another prometheus summary which counts the response time of each incoming requests.
This try to either use this as a middle ware or directly in the API.

You can measure the time by using `time.perf_counter()`. 