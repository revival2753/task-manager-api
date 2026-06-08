from fastapi import FastAPI, Request
from routers import tasks
import time
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

app.include_router(tasks.router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.method} {request.url} - {response.status_code} - {duration:.3f}s")
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()}
    )