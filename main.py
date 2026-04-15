@app.post("/request_phage")
def request_phage(req: Request):
    db = SessionLocal()
    phages = db.query(PhageDB).all()
    db.close()

    results = []

    for p in phages:
        score = 0

        host = (p.host_bacteria or "").lower()
        source = (p.source or "").lower()
        req_bacteria = (req.bacteria or "").lower()

        # Exact match
        if host == req_bacteria:
            score += 50

        # Partial match
        elif req_bacteria in host:
            score += 30

        # Lytic advantage
        if p.lytic:
            score += 20

        # Source preference
        if "lab" in source:
            score += 10

        results.append({
            "name": p.name,
            "host_bacteria": p.host_bacteria,
            "lab": p.lab,
            "score": score
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return {
        "request": {
            "clinician": req.clinician,
            "bacteria": req.bacteria,
            "urgency": req.urgency
        },
        "ranked_matches": results
    }
