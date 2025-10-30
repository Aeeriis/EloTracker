"""Persistent storage helpers for EloTracker."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List

DEFAULT_DATA_DIR = Path(os.environ.get("ELO_TRACKER_DATA_DIR", Path.home() / ".elo_tracker"))
DEFAULT_DATA_FILE = DEFAULT_DATA_DIR / "elo_history.json"


def ensure_storage_dir(path: Path = DEFAULT_DATA_DIR) -> None:
    """Create the storage directory if it does not exist."""
    path.mkdir(parents=True, exist_ok=True)


@dataclass
class EloDay:
    """Represents Elo progression for a single day."""

    date: date
    sets: List[int] = field(default_factory=list)

    @property
    def start(self) -> int | None:
        return self.sets[0] if self.sets else None

    @property
    def end(self) -> int | None:
        return self.sets[-1] if self.sets else None

    @property
    def change(self) -> int | None:
        if not self.sets:
            return None
        return self.sets[-1] - self.sets[0]

    @property
    def best(self) -> int | None:
        return max(self.sets) if self.sets else None

    @property
    def worst(self) -> int | None:
        return min(self.sets) if self.sets else None

    def to_dict(self) -> Dict[str, Iterable[int]]:
        return {"sets": self.sets}

    @classmethod
    def from_dict(cls, day: date, data: Dict[str, Iterable[int]]) -> "EloDay":
        sets = list(data.get("sets", []))
        return cls(date=day, sets=sets)


@dataclass
class EloData:
    """Represents the full Elo history."""

    days: Dict[str, EloDay] = field(default_factory=dict)

    def to_json(self) -> Dict[str, Dict[str, Iterable[int]]]:
        return {day: data.to_dict() for day, data in self.days.items()}

    @classmethod
    def from_json(cls, raw: Dict[str, Dict[str, Iterable[int]]]) -> "EloData":
        days: Dict[str, EloDay] = {}
        for day_str, value in raw.items():
            day_obj = date.fromisoformat(day_str)
            days[day_str] = EloDay.from_dict(day_obj, value)
        return cls(days=days)

    def get_day(self, day: date) -> EloDay:
        day_key = day.isoformat()
        if day_key not in self.days:
            self.days[day_key] = EloDay(date=day)
        return self.days[day_key]

    def sorted_days(self) -> List[EloDay]:
        return [self.days[day] for day in sorted(self.days.keys())]


def load_data(path: Path = DEFAULT_DATA_FILE) -> EloData:
    """Load Elo data from disk."""
    ensure_storage_dir(path.parent)
    if not path.exists():
        return EloData()
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return EloData.from_json(raw)


def save_data(data: EloData, path: Path = DEFAULT_DATA_FILE) -> None:
    """Persist Elo data to disk."""
    ensure_storage_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data.to_json(), f, indent=2, sort_keys=True)
