from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ✅ CORS FIX (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary storage
phages = []

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
    db = SessionLocal()
    phages = db.query(PhageDB).all()
    db.close()

    results = []

    for p in phages:
        score = 0

        # Exact match
        if p.host_bacteria.lower() == req.bacteria.lower():
            score += 50

        # Partial match
        elif req.bacteria.lower() in p.host_bacteria.lower():
            score += 30

        # Lytic advantage
        if p.lytic:
            score += 20

        # Source preference
        if "lab" in p.source.lower():
            score += 10

        results.append({
            "name": p.name,
            "host_bacteria": p.host_bacteria,
            "lab": p.lab,
            "score": score
        })

    # Sort by score (highest first)
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return {"request": req, "ranked_matches": results}
    matched = [p for p in phages if p.host_bacteria.lower() == req.bacteria.lower()]
    return {"request": req, "matches": matched}
# ---------------- USER SYSTEM ----------------

users = []

class User(BaseModel):
    username: str
    password: str
    role: str   # clinician or lab

@app.post("/register")
def register(user: User):
    users.append(user)
    return {"message": "User registered"}

@app.post("/login")
def login(user: User):
    for u in users:
        if u.username == user.username and u.password == user.password:
            return {"message": "Login successful", "role": u.role}
    return {"message": "Invalid credentials"}
