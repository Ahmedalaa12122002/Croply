from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")

# Serve static files
app.mount("/web", StaticFiles(directory=WEB_DIR), name="web")

@app.get("/")
def home():
    return FileResponse(os.path.join(WEB_DIR, "index.html"))
