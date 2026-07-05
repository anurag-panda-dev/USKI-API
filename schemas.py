"""
Pydantic schemas — what goes over the wire.
"""
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


# ---------- Victim stats (aggregate, not per-victim) ----------

class VictimStats(BaseModel):
    female: int = Field(0, ge=0)
    male: int = Field(0, ge=0)
    under_18: int = Field(0, ge=0, alias="under 18")
    age_18_30: int = Field(0, ge=0, alias="18-30")
    age_31_45: int = Field(0, ge=0, alias="31-45")
    age_46_60: int = Field(0, ge=0, alias="46-60")
    above_60: int = Field(0, ge=0, alias="above 60")
    major_occupation: Optional[str] = Field(None, description="Most common occupation among victims")

    model_config = ConfigDict(populate_by_name=True)

    @classmethod
    def from_any(cls, value):
        if value is None:
            return cls()
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            return cls.model_validate(value)
        return cls()


# ---------- Killer ----------

class KillerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    known_as: Optional[List[str]] = Field(default_factory=list, description="Aliases / nicknames")
    image_url: Optional[str] = Field(None, description="URL to a reference image")

    birth_year: Optional[int] = Field(None, ge=1000, le=2100)
    birth_location: Optional[str] = None

    murder_count_proved: int = Field(0, ge=0, description="Legally proven / convicted murder count")
    murder_count_actual: Optional[int] = Field(None, ge=0, description="Estimated true/suspected count")

    country: Optional[str] = None
    years_active_from: Optional[int] = None
    years_active_to: Optional[int] = None
    active_in_provinces: Optional[List[str]] = Field(default_factory=list)

    victim_stats: Optional[VictimStats] = Field(default_factory=VictimStats)

    method: Optional[str] = Field(None, description="Process / modus operandi, factual summary")
    sentence_details: Optional[str] = None
    motive: Optional[str] = Field(None, description="Reason for killing, if known or disclosed")

    additional_info: Optional[str] = None
    caught_by: Optional[str] = None


class KillerCreate(KillerBase):
    pass


class KillerUpdate(BaseModel):
    """All fields optional — partial update (PATCH-style via PUT)."""
    name: Optional[str] = None
    known_as: Optional[List[str]] = None
    image_url: Optional[str] = None
    birth_year: Optional[int] = None
    birth_location: Optional[str] = None
    murder_count_proved: Optional[int] = None
    murder_count_actual: Optional[int] = None
    victim_stats: Optional[VictimStats] = None
    country: Optional[str] = None
    years_active_from: Optional[int] = None
    years_active_to: Optional[int] = None
    active_in_provinces: Optional[List[str]] = None
    method: Optional[str] = None
    sentence_details: Optional[str] = None
    motive: Optional[str] = None
    additional_info: Optional[str] = None
    caught_by: Optional[str] = None


class ScoreBreakdown(BaseModel):
    brutality: float
    evasion: float
    notoriety: float
    psychopathy: float


class ScoreResponse(BaseModel):
    killer_id: str
    psycho_killer_score: float
    breakdown: Optional[ScoreBreakdown] = None


class KillerOut(KillerBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    psycho_killer_score: float
    score_breakdown: ScoreBreakdown
