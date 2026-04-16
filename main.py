from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATABASE
engine = create_engine("sqlite:///./phage.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# TABLES
class PhageDB(Base):
    __tablename__ = "phages"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    host_bacteria = Column(String)
    source = Column(String)
    lytic = Column(Boolean)
    lab = Column(String)

Base.metadata.create_all(bind=engine)

# SCHEMAS
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

# ROUTES

@app.get("/")
def home():
    return {"message": "API Running"}

@app.post("/add_phage")
def add_phage(phage: Phage):
    db = SessionLocal()
    db.add(PhageDB(**phage.dict()))
    db.commit()
    db.close()
    return {"message": "Phage added"}

@app.post("/request_phage")
def request_phage(req: Request):
    db = SessionLocal()
    phages = db.query(PhageDB).all()
    db.close()

    results = []

    for p in phages:
        host = (p.host_bacteria or "").lower()
        source = (p.source or "").lower()
        req_bacteria = (req.bacteria or "").lower()

        score = 0

        if host == req_bacteria:
            score += 50
        elif req_bacteria in host:
            score += 30

        if p.lytic:
            score += 20

        if "lab" in source:
            score += 10

        results.append({
            "name": p.name,
            "score": score
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return {"ranked_matches": results}
