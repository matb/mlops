import onnxruntime as rt
import fastapi
import uvicorn

app = fastapi.FastAPI()


@app.on_event("startup")
def load_onnx():
    # TODO change this
    app.state.model_session = ""


@app.get("/iris/prediction")
def predic_iris_class(sepal_length: float= fastapi.Query(),
                      ... ): #TODO Add your code here
    sess = app.state.model_session
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    
    # TODO change this
    pred_onx = sess.run([label_name], {input_name: ""})[0]

    res = [float(x) for x in pred_onx.tolist()]
    return {"predictions": res}


if __name__ == '__main__':
    uvicorn.run(app)