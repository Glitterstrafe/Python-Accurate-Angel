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

    def read_all(self, limit: int = 1000) -> List[AngelEvent]:
        """
        Read recent events from the chronicles.
        Used for rebuilding state; defaults to a safe tail to avoid unbounded memory use.
        """
        if limit is None:
            limit = 1000

        if limit <= 0:
            return []

        events = []
        if not self.chronicles_path.exists():
            return events

        for line in self._read_tail_lines(limit):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                events.append(AngelEvent(**data))
            except (json.JSONDecodeError, ValueError):
                continue
        return events

    def read_since(self, timestamp: str) -> List[AngelEvent]:
        """Read events after a given timestamp."""
        events: List[AngelEvent] = []
        if not self.chronicles_path.exists():
            return events

        with open(self.chronicles_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    event = AngelEvent(**data)
                except (json.JSONDecodeError, ValueError):
                    continue
                if event.timestamp > timestamp:
                    events.append(event)
        return events

    def _read_tail_lines(self, limit: int, chunk_size: int = 4096) -> List[str]:
        if limit <= 0:
            return []

        with open(self.chronicles_path, "rb") as f:
            f.seek(0, os.SEEK_END)
            position = f.tell()
            buffer = b""
            lines: List[bytes] = []

            while position > 0 and len(lines) <= limit:
                read_size = min(chunk_size, position)
                position -= read_size
                f.seek(position)
                chunk = f.read(read_size)
                buffer = chunk + buffer
                lines = buffer.splitlines()

            tail = lines[-limit:]
            return [line.decode("utf-8", errors="replace") for line in tail]

    def get_last_event(self) -> Optional[AngelEvent]:
        """Get the most recent event."""
        events = self.read_all(limit=1)
        return events[-1] if events else None

    def count(self) -> int:
        """Count total events in the chronicles."""
        if not self.chronicles_path.exists():
            return 0

        count = 0
        with open(self.chronicles_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    count += 1
        return count
