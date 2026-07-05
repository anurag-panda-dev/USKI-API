"""
CRUD operations — the only layer that talks directly to the DB session.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

try:
    import models, schemas
except ImportError:  # pragma: no cover - supports direct script execution
    import models
    import schemas


def create_killer(db: Session, payload: schemas.KillerCreate) -> models.Killer:
    data = payload.model_dump()
    victim_stats = payload.victim_stats
    if victim_stats is None:
        data["victim_stats"] = {}
    else:
        data["victim_stats"] = victim_stats.model_dump(by_alias=True)
    killer = models.Killer(**data)
    db.add(killer)
    db.commit()
    db.refresh(killer)
    return killer


def get_killer(db: Session, killer_id: int) -> Optional[models.Killer]:
    return db.query(models.Killer).filter(models.Killer.id == killer_id).first()


def list_killers(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    country: Optional[str] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
) -> List[models.Killer]:
    query = db.query(models.Killer)
    if country:
        query = query.filter(models.Killer.country.ilike(f"%{country}%"))
    if name:
        query = query.filter(
            or_(
                models.Killer.name.ilike(f"%{name}%"),
            )
        )
    return query.offset(skip).limit(limit).all()


def update_killer(db: Session, killer: models.Killer, payload: schemas.KillerUpdate) -> models.Killer:
    updates = payload.model_dump(exclude_unset=True)
    if updates.get("victim_stats") is not None:
        updates["victim_stats"] = payload.victim_stats.model_dump(by_alias=True)
    for field, value in updates.items():
        setattr(killer, field, value)
    db.commit()
    db.refresh(killer)
    return killer


def delete_killer(db: Session, killer: models.Killer) -> None:
    db.delete(killer)
    db.commit()
