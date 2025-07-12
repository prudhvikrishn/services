from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import csv
from datetime import datetime
from fastapi.responses import HTMLResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FormData(BaseModel):
    name: str
    phone: str
    email: str
    service: str
    details: str

CSV_FILE = "service_requests.csv"

@app.post("/submit")
async def submit_form(data: FormData):
    try:
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
    except Exception as e:
        return {"error": f"Error saving to CSV: {e}"}

@app.get("/", response_class=HTMLResponse)
async def serve_form():
    try:
        with open("form.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="<h1>form.html not found</h1>", status_code=500)
