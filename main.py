from fastapi import FastAPI, Request
from routers import tasks
import time

app = FastAPI()

app.include_router(tasks.router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.method} {request.url} - {response.status_code} - {duration:.3f}s")
    return response
