"""
SQLAlchemy ORM models — the actual database tables.
Victim details are stored as aggregate counts (not per-victim records) on the
killer row itself: sex counts, age-bracket counts, and a single free-text
"major occupation" summary.
"""
from sqlalchemy import Column, Integer, String, Text, JSON

from database import Base


class Killer(Base):
    __tablename__ = "killers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, index=True)
    known_as = Column(JSON, nullable=True)          # list[str] of aliases/nicknames
    image_url = Column(String, nullable=True)

    birth_year = Column(Integer, nullable=True)
    birth_location = Column(String, nullable=True)

    murder_count_proved = Column(Integer, default=0)     # legally proven/convicted count
    murder_count_actual = Column(Integer, nullable=True)  # estimated/suspected true count

    # Aggregate victim breakdown — see schemas.VictimStats for the shape:
    # {"female": int, "male": int, "under_18": int, "18-30": int, "31-45": int,
    #  "46-60": int, "above_60": int, "major_occupation": str}
    victim_stats = Column(JSON, nullable=True)

    country = Column(String, nullable=True, index=True)
    years_active_from = Column(Integer, nullable=True)
    years_active_to = Column(Integer, nullable=True)
    active_in_provinces = Column(JSON, nullable=True)      # list[str]

    method = Column(Text, nullable=True)             # modus operandi / process, factual summary
    sentence_details = Column(Text, nullable=True)   # verdict, sentence, fate
    motive = Column(Text, nullable=True)             # reason for killing, if known/disclosed

    additional_info = Column(Text, nullable=True)
    status = Column(String, nullable=True)           # "convicted" | "suspected" | "unidentified" | "deceased"
    caught_by = Column(String, nullable=True)         # how they were caught / case-breaking detail
