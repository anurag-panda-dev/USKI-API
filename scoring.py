"""
A simpler severity heuristic for the USKI API.

This score is meant to be transparent and useful even when some fields are
missing. It focuses on four observable signals that are usually available:

1. confirmed or estimated victim count
2. how long the offending pattern lasted
3. whether the case is still active or unresolved
4. whether the case description suggests a highly organized or persistent method

It does not depend on male/female counts or age brackets.
"""
import math
from typing import Optional

import models
import schemas


def _get_stats(killer: models.Killer) -> schemas.VictimStats:
    raw = killer.victim_stats or {}
    return schemas.VictimStats.from_any(raw)


def _count_signal(killer: models.Killer) -> float:
    actual = killer.murder_count_actual or killer.murder_count_proved or 0
    proved = killer.murder_count_proved or 0
    if actual <= 0:
        return 0.0
    return min(45.0, (actual * 2.0) + (proved * 0.3))


def _duration_signal(killer: models.Killer) -> float:
    year_from = killer.years_active_from
    year_to = killer.years_active_to
    if year_from and year_to and year_to >= year_from:
        span = max(1, year_to - year_from + 1)
        return min(15.0, span * 0.8)
    return 0.0


def _evasion_signal(killer: models.Killer) -> float:
    actual = killer.murder_count_actual or killer.murder_count_proved or 0
    proved = killer.murder_count_proved or 0
    if actual > proved and actual > 0:
        return min(12.0, 2.0 + (actual - proved) * 1.5)
    if proved >= 5:
        return min(10.0, 1.5 + proved * 0.8)
    return 0.0


def _notoriety_signal(killer: models.Killer) -> float:
    actual = killer.murder_count_actual or killer.murder_count_proved or 0
    proved = killer.murder_count_proved or 0
    additional_info = (killer.additional_info or "").lower()
    birth_location = (killer.birth_location or "").strip()

    score = 0.0

    if actual > 0:
        score += min(6.0, actual * 0.4)
    if proved > 0:
        score += min(4.0, proved * 0.2)

    if any(token in additional_info for token in ["notorious", "famous", "widely known", "publicized", "media", "infamous"]):
        score += 3.0

    if birth_location:
        score += 0.5

    return min(10.0, round(score, 2))


def _psychopathy_signal(killer: models.Killer) -> float:
    method = (killer.method or "").lower()
    additional_info = (killer.additional_info or "").lower()
    birth_year = killer.birth_year
    birth_location = (killer.birth_location or "").strip()

    score = 0.0

    if not method and not additional_info:
        return 0.0

    if any(token in method for token in ["lured", "planned", "organized", "control", "systematic", "calculated", "methodical"]):
        score += 6.0
    elif any(token in method for token in ["stalked", "targeted", "strangled", "poisoned", "dismembered"]):
        score += 4.0

    if any(token in additional_info for token in ["planned", "organized", "calculated", "systematic", "evasion", "avoid", "eluded", "repeat"]):
        score += 3.0

    if birth_year and birth_year >= 1950:
        score += 0.5

    if birth_location:
        score += 0.5

    return min(10.0, round(score, 2))


def calculate(killer: models.Killer) -> schemas.ScoreBreakdown:
    stats = _get_stats(killer)
    count_signal = _count_signal(killer)
    duration_signal = _duration_signal(killer)
    evasion_signal = _evasion_signal(killer)
    notoriety_signal = _notoriety_signal(killer)
    psychopathy_signal = _psychopathy_signal(killer)

    return schemas.ScoreBreakdown(
        brutality=round(count_signal, 2),
        evasion=round(evasion_signal, 2),
        notoriety=round(notoriety_signal, 2),
        psychopathy=round(psychopathy_signal, 2),
    )


def build_score_response(killer: models.Killer) -> schemas.ScoreResponse:
    breakdown = calculate(killer)
    raw = breakdown.brutality + breakdown.evasion + breakdown.notoriety + breakdown.psychopathy
    final = min(100.0, round(100 * (1 - math.exp(-raw / 28.0)), 2))

    return schemas.ScoreResponse(
        killer_id=str(killer.id),
        psycho_killer_score=final,
        breakdown=breakdown,
    )
