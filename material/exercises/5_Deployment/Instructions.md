# Demo

This demo will reuse the container approach of serving a tensorflow model and show how a potential canary deployment could look like
with the following Setup: 

- create_models.py is generating two versions of our model - v1 and v2. Lets see v2 as an updated version that we want to canary deploy. 
- V1 will always return 0 while v2 will always return 1 s.t. we can differentiate where the response came from 
- We will start of by having a docker compose setup with a tensorflow-serving container  exposing v1 
- Infront we will have Nginx as a Load-balancer.
- At first, we can deploy the model as is by hitting `docker compose up -d `
- Using main.py we will be able to see we get the expected answer back - 0 
- Now let change our docker-compose file and add our new server and edit our Nginx config
```docker-compose
  tf_service_2:
    image: tensorflow/serving:2.11.0
    container_name: tf_service_2
    volumes:
      - ./model2/:/models/
    ports:
      - "8502:8500"
      - "8503:8501"
    command:
      - '--model_config_file=/models/models.config'
      - '--allow_version_labels_for_unavailable_models=true'
      - '--model_config_file_poll_wait_seconds=60'
      - '--rest_api_port=8501'
    networks:
      - default_network
```
```config
    upstream backend {
    server tf_service_1:8501 weight=9;
    server tf_service_2:8501 weight=1;
    }
```

- Now you can update the compose via `docker compose up -d`
- This will start the new version of our api next to the v1. 
- Finally, giving Nginx a restart to reread our config `docker compose restart nginx`

Note: In a real production environment one would use a Service-mesh to directly track changes of service versions to skip the restart of the Load-balancer. 