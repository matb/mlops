import time

from prometheus_client import Counter, Summary
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette_prometheus import PrometheusMiddleware

RequestCounter = Counter(
    "custom_request_counter",
    "Custom counter for requests",
    ["method", "path_template"],
)

SuccessSummary = Summary(
    "custom_success_summary",
    "Summary of the successful requests",
    ["method", "path_template"],
)

TimeSummary = Summary(
    "request_time_summary",
    "Summary of the time a requests took",
    ["method", "path_template"],
)


class MetricMiddleware(PrometheusMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        method = request.method
        path_template, is_handled_path = self.get_path_template(request)

        if self._is_path_filtered(is_handled_path):
            return await call_next(request)
        RequestCounter.labels(
            method=method, path_template=request.url.path
        ).inc(1)
        response = await call_next(request)
        if 200 <= response.status_code < 400:
            SuccessSummary.labels(method=method, path_template=path_template).observe(1)
        return response


class TimeMiddleware(PrometheusMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start = time.perf_counter()
        method = request.method
        path_template, is_handled_path = self.get_path_template(request)

        if self._is_path_filtered(is_handled_path):
            return await call_next(request)

        response = await call_next(request)
        TimeSummary.labels(method=method, path_template=path_template).observe(time.perf_counter() - start)
        return response
