---

###`DEV_LOG_003_01312026.md`

```markdown
# 📜 Dev Log 003: Schema Gravity
**Date:** January 31, 2026
**Topic:** Implementing v0.3 "Slots Ready" Architecture
**Status:** SCHEMA LOCKED

## 1. The Pivot to Event Sourcing
Following architectural review, we identified that storing the graph state directly is fragile. 
We have moved to an **Event Sourced** model. 
* **Old Way:** Watch file -> Update Graph.
* **New Way:** Watch file -> Log Event -> Rebuild Graph from Log.

## 2. Technical Upgrades
* **JSONL:** We switched logs to JSON Lines for atomic appends.
* **Pydantic:** We implemented `angel/types.py` to strictly define `Proposal` and `AngelEvent` objects. This prevents "schema drift" where the data gets messy over time.
* **Rebuild Logic:** `wheels.py` now includes a `rebuild_from_chronicles()` function that replays the entire project history on startup.

## 3. Why This Matters
This allows "Time Travel." In the future, we can ask the Angel: *"Show me what the system looked like last Tuesday."* Because we have the event log, we can just replay events up to that timestamp.
