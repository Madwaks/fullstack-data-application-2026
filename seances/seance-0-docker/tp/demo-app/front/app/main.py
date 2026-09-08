import os

import httpx
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

API_URL = os.environ.get("API_URL", "http://localhost:8000")

app = FastAPI(title="TP Séance 0 - Front")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def hello(request: Request):
    try:
        response = httpx.get(API_URL, timeout=3.0)
        api_message = response.json()["message"]
    except httpx.HTTPError:
        api_message = "impossible de contacter l'api"
    return templates.TemplateResponse(
        request, "index.html", {"api_message": api_message}
    )
