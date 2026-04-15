from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# In-memory database (temporary)
phages = []
requests = []

class Phage(BaseModel):
    name: str
    host_bacteria: str
    source: str
    lytic: bool
    lab: str

class Request(BaseModel):
    clinician: str
    bacteria: str
    urgency: str

@app.get("/")
def home():
    return {"message": "Phage Directory API Running"}

@app.post("/add_phage")
def add_phage(phage: Phage):
    phages.append(phage)
    return {"message": "Phage added successfully"}

@app.get("/list_phages")
def list_phages():
    return phages

@app.post("/request_phage")
def request_phage(req: Request):
    matched = [p for p in phages if p.host_bacteria.lower() == req.bacteria.lower()]
    response = {
        "request": req,
        "matches": matched
    }
    requests.append(response)
    return response