"""Small reusable helpers for tests (kept out of conftest.py on purpose:
conftest is for fixtures, normal modules are for plain functions/classes)."""

import uuid
from dataclasses import dataclass


@dataclass
class Medicine:
    """Simple container for test medicine data."""

    name: str
    hour: str = "08"
    minute: str = "00"
    period: str = "AM"


def unique_name(prefix: str = "AutoMed") -> str:
    """Random name like 'AutoMed3fa9c1' so tests never clash with each other or real data.
    (Only letters/numbers - the app's add form rejects other special characters.)"""
    return f"{prefix}{uuid.uuid4().hex[:6]}"