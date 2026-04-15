@app.post("/request_phage")
def request_phage(req: Request):
    db = SessionLocal()
    phages = db.query(PhageDB).all()
    db.close()

    results = []

    for p in phages:
        try:
            host = str(p.host_bacteria or "").lower()
            source = str(p.source or "").lower()
            req_bacteria = str(req.bacteria or "").lower()

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
                "host_bacteria": p.host_bacteria,
                "score": score
            })

        except Exception as e:
            # Skip bad data
            continue

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return {"ranked_matches": results}
