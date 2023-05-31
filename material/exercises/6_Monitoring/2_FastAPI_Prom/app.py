import os
import uuid

import joblib
import pandas as pd
import pendulum
import pydantic
import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from loguru import logger
from starlette.middleware import Middleware
from starlette_prometheus import PrometheusMiddleware, metrics

import middleware

app = FastAPI(
    title="UTA MLOps API",
    version="0.1.0",
    docs_url="/docs",
    description="RESTApi to retrieve data and metrics",
    debug=True,
    root_path=os.getenv("API_ROOT_PATH", ""),
    middleware=[
        Middleware(middleware.MetricMiddleware),
        Middleware(PrometheusMiddleware),
    ],
)


class PredictionRequest(pydantic.BaseModel):
    """
    This will be our request model what we expect a user to provide
    Moreover, fastapi will directly transform a Swagger interface out of this
    """
    age: int
    workclass: str
    education: str
    education_num: int
    marital_status: str
    race: str
    sex: str
    hours_per_week: int


@app.middleware("http")
async def set_id(request: Request, call_next):
    request.state.id = str(uuid.uuid4())
    response = await call_next(request)
    return response


@app.on_event("startup")
async def startup():
    app.state.start = pendulum.now()
    app.state.model = joblib.load("models/model.joblib")
    logger.info(f"API started at {app.state.start}.")


app.add_route("/metrics/", metrics)


@app.post("/rest/on-demand/v1/income/prediction")
async def _(
        request: Request,
        data: PredictionRequest
):
    """

    """

    job_id = request.state.id

    logger.info(f"{job_id}| Data: {data}.")
    prediction = app.state.model.predict(pd.DataFrame({
        'age': data.age,
        'workclass': data.workclass,
        'education': data.education,
        'education_num': data.education_num,
        'marital_status': data.marital_status,
        'race': data.race,
        'sex': data.sex,
        'hours_per_week': data.hours_per_week
    },
        index=[0]))
    map = {0: '<=50K',
           1: '>50K'}
    res = map[prediction[0]]
    logger.info(f"{job_id}| Response : {prediction}")
    return res


@app.get("/metrics/v1/healthCheck")
def health_check(request: Request):
    now = pendulum.now()
    uptime = now - request.app.state.start
    msg = {
        "healthy": 1,
        "api": {
            "started": request.app.state.start.diff_for_humans(),
        },
        "server-time-started": request.app.state.start,
        "server-time-current": now,
        "server-uptime": uptime,
    }
    return msg


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
