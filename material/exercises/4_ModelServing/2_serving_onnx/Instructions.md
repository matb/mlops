# Instructions 

Now you are going to deploy the onnx model from earlier using FastAPI. 

1. Copy over the model that was generated in 3_ModelSaving or  copy over the model.py and b_ONNX.py and execute them again. 
2. look into app.py and finish the `on_even` wrapped functions by loading the model and attach it to the session. 
    1. Remember you can load the model via `onnxruntime.InferenceSession("model.onnx")`
3. Finish the `prediction` function by finishing the input we need from the user 
    1. we need four values  (sepal, petal) x (length, width)
   2. Put the values nested in a list and hand it as input to the `run` function
4. Run the server by executing the file 
5. Go to the swagger UI (http://127.0.0.1:8000/docs) and try out a requests or use the following curl
```bash 
curl -X 'GET' \
  'http://127.0.0.1:8000/iris/prediction?sepal_length=1&sepal_width=1&petal_length=1&petal_width=1' \
  -H 'accept: application/json'
```