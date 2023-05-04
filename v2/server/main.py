from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/echo/{message}")
async def echo(message: str):
    return {"message": message}
