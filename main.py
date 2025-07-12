from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import csv
import os

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (logo, CSS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define data model
class FormData(BaseModel):
    name: str
    phone: str
    email: str
    service: str
    details: str

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "service_requests.csv")
HTML_FILE = os.path.join(BASE_DIR, "form.html")

@app.post("/submit")
async def submit_form(data: FormData):
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.name,
            data.phone,
            data.email,
            data.service,
            data.details
        ])
    return {"message": "Submitted successfully"}

@app.get("/", response_class=HTMLResponse)
async def serve_form():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return f.read()
