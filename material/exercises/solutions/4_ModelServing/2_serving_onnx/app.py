import onnxruntime as rt
import fastapi
import uvicorn

app = fastapi.FastAPI()


@app.on_event("startup")
def load_onnx():

    app.state.model_session = rt.InferenceSession("model.onnx")


@app.get("/iris/prediction")
def predic_iris_class(sepal_length: float= fastapi.Query(),
                      sepal_width: float= fastapi.Query(),
                      petal_length: float= fastapi.Query(),
                      petal_width: float= fastapi.Query()):
    sess = app.state.model_session
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    pred_onx = sess.run([label_name], {input_name: [[sepal_length, sepal_width,
                                                    petal_length, petal_width]]})[0]

    res = [float(x) for x in pred_onx.tolist()]
    return {"predictions": res}


if __name__ == '__main__':
    uvicorn.run(app)