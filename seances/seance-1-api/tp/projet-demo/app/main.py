from fastapi import FastAPI

app = FastAPI(title="GearShare API", version="0.1.0")


@app.get("/health", tags=["monitoring"])
def health() -> dict[str, str]:
    return {"status": "ok"}
