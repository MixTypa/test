import subprocess

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, CONTENT_TYPE_LATEST, generate_latest

app = FastAPI()

REQUESTS = Counter("app_requests_total", "Количество запросов", ["endpoint"])


@app.post("/")
def index(request: Request):
    REQUESTS.labels(endpoint="/").inc()
    if request.headers.get("Test") == "Hello":
        return PlainTextResponse("Hello, World!")
    raise HTTPException(status_code=403, detail="Нужен заголовок Test: Hello")


@app.get("/health")
def health():
    REQUESTS.labels(endpoint="/health").inc()
    result = subprocess.run(["ping", "-c", "1", "-W", "2", "77.88.8.8"], capture_output=True)
    if result.returncode == 0:
        return PlainTextResponse("OK", status_code=200)
    return PlainTextResponse("PING FAILED", status_code=503)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
