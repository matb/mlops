Exercise: TensorFlow Serving with a Simple Linear Regression Model

In this exercise, you will use TensorFlow Serving to serve a simple linear regression model. You will need to complete the following steps:

    Create a simple linear regression model using TensorFlow
    Export the model in the SavedModel format
    Start TensorFlow Serving and load the exported model
    Send a prediction request to the server and display the result

Instructions:

1. Go to the file named "model.py" and  in-comment the  code that defines a simple linear regression model using TensorFlow.
2. Note that we are saving the model under models/<NAME>/<Version> 
3.  Try to run the model using tensorflow serving API:
    ```bash 
    tensorflow_model_server --port=8500 --model_name=iris --model_base_path=</path/to/saved_model>
    ```
Note: tensorflow_model_server is an apt-package 


## Demo
For proper deployment we would use a container - e.g. by extending the prebuild tensorflow serving container. 
Therefor we have next to the models itself a configuration that specifies what and how we want to serve it. 
The models/models.config contains these instructions that we just did via cli: 

```config
model_config_list {
    config {
        name: "iris",
        base_path: "/models/iris/"
        model_platform: "tensorflow"
        model_version_policy { all: {}}
    }
}
```
To start a server from this container we can either first build the container using the small docker file and create a storable artifact 
or directly launch it using: 
```docker 
docker run -ti --rm -p 8501:8501 -p 8500:8500\
         --name=serving \
             -v "$(pwd)/models/:/models/" \
             tensorflow/serving:2.11.0 \
             --model_config_file=/models/models.config \
             --allow_version_labels_for_unavailable_models=true \
             --model_config_file_poll_wait_seconds=60
```
