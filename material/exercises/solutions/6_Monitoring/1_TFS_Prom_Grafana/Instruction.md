# Demo

This small demo will take our earlier TF Serving example and extend it using prometheus to access performance metrics
from
our server and scrape them to be visualized in Grafana.

1. Please execute the `create_models.py` as they are the basis for this demo

- We will look into the new monitoring.config in our models folder

```config
prometheus_config {
  enable: true,
  path: "/monitoring/prometheus/metrics"
}
```

- Here we define that we want to expose prometheus metrics via the endpoint `/monitoring/prometheus/metrics`
- In the prometheus_docker_compose.yml we then define the counterpart that prometheus should scrape that endpoint every
  5 seconds.

2. Now we can start the composition via `docker compose up`

### Prometheus

3. Navigate the browser to localhost:9090

- In the Query-Prompt (Expression) you can see als potential results related to tensorflow by just typing `:tensorflow:`

### Grafana

4. Now we can go to grafana that will be hosted on localhost:3000 using the user:password admin:admin

- first we need to add the datasource prometheus. Please navigate via the hamburger-menu to administration and
  datasources
- There click "Add a new DataSource" and chose "Prometheus"
- There you need to add the connection details - here we need to only change the url to `http://prometheus.:9090`
- Now please jump back to the burger-menu and go to Dashboards
- Here you find "New" and select "Dashboard" and "New Visualization"
- There we can now easily visualize the metrics and adding prometheus as a data source and refer to the exposed
  metrics `:tensorflow...`