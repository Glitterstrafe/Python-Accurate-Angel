import json
import os
from typing import List, Optional
from pathlib import Path
from .types import AngelEvent


class TheScribe:
    """
    The Chronicles keeper. Handles append-only JSONL event storage.
    This is the ground truth - everything else is derived.
    """

    def __init__(self, chronicles_path: str = "angel_chronicles.jsonl"):
        self.chronicles_path = Path(chronicles_path)
        self._ensure_chronicles_exist()

    def _ensure_chronicles_exist(self):
        """Create the chronicles file if it doesn't exist."""
        if not self.chronicles_path.exists():
            self.chronicles_path.touch()

    def record(self, event: AngelEvent) -> None:
        """
        Append an event to the chronicles.
        Atomic write - each event is one line.
        """
        with open(self.chronicles_path, "a", encoding="utf-8") as f:
            f.write(event.model_dump_json() + "\n")

    def read_all(self) -> List[AngelEvent]:
        """
        Read all events from the chronicles.
        Used for rebuilding state.
        """
        events = []
        if not self.chronicles_path.exists():
            return events

        with open(self.chronicles_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        events.append(AngelEvent(**data))
                    except (json.JSONDecodeError, ValueError):
                        # Skip malformed lines
                        continue
        return events

    def read_since(self, timestamp: str) -> List[AngelEvent]:
        """Read events after a given timestamp."""
        all_events = self.read_all()
        return [e for e in all_events if e.timestamp > timestamp]

    def get_last_event(self) -> Optional[AngelEvent]:
        """Get the most recent event."""
        events = self.read_all()
        return events[-1] if events else None

    def count(self) -> int:
        """Count total events in the chronicles."""
        return len(self.read_all())
