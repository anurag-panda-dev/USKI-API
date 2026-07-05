"""
Serial Killer Information API
==============================
A FastAPI reference/database service for structured, factual information
about (historical, publicly documented) serial killer cases — similar in
spirit to a structured Wikipedia infobox exposed as an API.

Run with:
    uvicorn app.main:app --reload
Then open:
    http://127.0.0.1:8000/docs   (interactive Swagger UI)
"""
import math
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session


import models
import schemas
import crud
import scoring
from database import engine, get_db, Base

app = FastAPI(
    title="Serial Killer Information API",
    description=(
        "Structured reference data on serial killer cases: identity, aggregate "
        "victim stats, timeline, method, sentencing, and a computed 'Psycho Killer Score'."
    ),
    version="1.1.0",
)


def _to_out(killer: models.Killer) -> schemas.KillerOut:
    """Build the response schema, injecting the computed score fields.

    Missing values are handled gracefully so the API still returns a complete
    response even when the source data is sparse.
    """
    breakdown = scoring.calculate(killer)
    base = schemas.KillerBase.model_validate(killer).model_dump()
    base.setdefault("victim_stats", {})
    if isinstance(base["victim_stats"], dict):
        base["victim_stats"] = schemas.VictimStats.from_any(base["victim_stats"]).model_dump(by_alias=True)
    return schemas.KillerOut(
        **base,
        id=killer.id,
        psycho_killer_score=round(
            100 * (1 - math.exp(-(breakdown.brutality + breakdown.evasion + breakdown.notoriety + breakdown.psychopathy) / 28.0)),
            2,
        ),
        score_breakdown=breakdown,
    )


def _get_killer_or_404(db: Session, killer_id: int) -> models.Killer:
    killer = crud.get_killer(db, killer_id)
    if not killer:
        raise HTTPException(status_code=404, detail=f"Killer with id {killer_id} not found")
    return killer


# ---------------------------------------------------------------------------
# Killers
# ---------------------------------------------------------------------------

@app.post("/killers", response_model=schemas.KillerOut, status_code=status.HTTP_201_CREATED, tags=["Killers"])
def create_killer(payload: schemas.KillerCreate, db: Session = Depends(get_db)):
    """Create a new killer record, with aggregate victim_stats (counts + major occupation)."""
    killer = crud.create_killer(db, payload)
    return _to_out(killer)


@app.get("/killers", response_model=List[schemas.KillerOut], tags=["Killers"])
def list_killers(
    skip: int = 0,
    limit: int = Query(100, ge=1, le=1000),
    country: Optional[str] = Query(None, description="Filter by country (partial match)"),
    name: Optional[str] = Query(None, description="Filter by name (partial match)"),
    min_score: Optional[float] = Query(None, ge=0, le=100, description="Minimum psycho_killer_score"),
    db: Session = Depends(get_db),
):
    """List killers with optional filters. Results are paginated (skip/limit)."""
    killers = crud.list_killers(db, skip, limit, country, name, None)
    results = [_to_out(k) for k in killers]
    if min_score is not None:
        results = [r for r in results if r.psycho_killer_score >= min_score]
    return results


@app.get("/killers/{killer_id}", response_model=schemas.KillerOut, tags=["Killers"])
def get_killer(killer_id: int, db: Session = Depends(get_db)):
    killer = _get_killer_or_404(db, killer_id)
    return _to_out(killer)


@app.put("/killers/{killer_id}", response_model=schemas.KillerOut, tags=["Killers"])
def update_killer(killer_id: int, payload: schemas.KillerUpdate, db: Session = Depends(get_db)):
    killer = _get_killer_or_404(db, killer_id)
    killer = crud.update_killer(db, killer, payload)
    return _to_out(killer)


@app.delete("/killers/{killer_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Killers"])
def delete_killer(killer_id: int, db: Session = Depends(get_db)):
    killer = _get_killer_or_404(db, killer_id)
    crud.delete_killer(db, killer)
    return None


@app.get("/killers/{killer_id}/score", response_model=schemas.ScoreResponse, tags=["Killers"])
def get_score_breakdown(killer_id: int, db: Session = Depends(get_db)):
    """Return the psycho_killer_score in the new score-response shape."""
    killer = _get_killer_or_404(db, killer_id)
    return scoring.build_score_response(killer)


# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------

@app.get("/", tags=["Misc"])
def root():
    return {
        "message": "Serial Killer Information API",
        "docs": "/docs",
        "note": "Educational / true-crime reference dataset. Data must be sourced from public, verifiable records.",
    }
