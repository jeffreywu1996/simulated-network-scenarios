import os
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import Optional


class Log(BaseModel):
    id: Optional[str]
    n: Optional[int]
    payload: Optional[str]
    topic: Optional[str]
    producer_id: Optional[str]
    consumer_id: Optional[str]
    sent_timestamp: Optional[int]
    recieve_timestamp: Optional[int]


app = FastAPI(title="Log Server API", openapi_url="/openapi.json")
api_router = APIRouter()

l = list()

@api_router.get("/hash", status_code=200)
def get_testhash() -> str:
    return os.getenv('TEST_HASH')


@api_router.post("/log", status_code=200)
def log_action(log: Log) -> dict:
    """
    Logs action
    """
    l.append(log)
    return {"result": "success"}


@api_router.get("/logs", status_code=200)
def log_list() -> dict:
    """
    Get all logs
    """
    return l


@api_router.get("/clear", status_code=200)
def log_list() -> dict:
    global l
    l = list()
    return {"result": "success"}


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
