from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")

app = FastAPI(title="TSAS")

# Serve JS files
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")

@app.get("/")
def root():
    return FileResponse(os.path.join(WEB_DIR, "index.html"))
