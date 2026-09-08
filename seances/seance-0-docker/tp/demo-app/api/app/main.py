from fastapi import FastAPI

app = FastAPI(title="TP Séance 0 - API")


@app.get("/")
def hello() -> dict:
    return {"message": "Hello from api!"}
