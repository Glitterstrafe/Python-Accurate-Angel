
### 1. `Tech_Specifications_v03.md`

```markdown
# 📐 Technical Specifications v03: The Event-Sourced Witness
**Version:** 0.3 (Slots Ready)
**Date:** January 31, 2026
**Architecture:** Event Sourced / Pydantic Typed

## 1. System Philosophy
* **Immutable History:** The state of the system is derived entirely from `angel_chronicles.jsonl`. We can delete the graph and rebuild it perfectly from the logs.
* **Structured Proposals:** The AI does not modify the graph. It yields a `Proposal` object. The Human (via CLI) converts the Proposal into a `CONFIRMED` event.
* **Intent Nodes:** Code links to fuzzy human intents ("Make it flowy"), which are treated as first-class nodes in the graph.

## 2. Data Models (`angel/types.py`)
We enforce strict typing using Pydantic.

### The Proposal
```python
class Proposal(BaseModel):
    proposal_id: str
    work_unit_id: str
    confidence: float
    edge: EdgeDef  # { source: "main.py", target: "Reduce Jitter", type: "implements" }
    rationale: str

```

### The Event (Log Entry)

```python
class AngelEvent(BaseModel):
    event_id: str
    timestamp: str
    action_type: Literal["WORK_UNIT_CAPTURED", "PROPOSAL_GENERATED", "PROPOSAL_CONFIRMED", "PROPOSAL_REJECTED"]
    # ...contextual fields (proposal_id, explicit_approval, etc.)

```

## 3. Storage Architecture

* **`angel_chronicles.jsonl`:** The ground truth. Append-only. Atomic writes.
* **`angel_state.json` (Optional):** A derived cache of the current graph state for performance (rebuildable).

## 4. Module Responsibilities

* **`angel/chronicles.py` (The Scribe):** Handles low-level JSONL reading/writing.
* **`angel/wheels.py` (The Sephirot):** Contains `rebuild_from_chronicles(events)`. It replays the event stream to construct the `NetworkX` graph in memory.
* **`angel/voice.py` (The Herald):** Visualizes the `Proposal` object using Rich tables.

## 5. Implementation Roadmap

* [x] **Phase 1: Genesis** (MVP File Watching)
* [x] **Phase 2: Ascension** (v0.3 Schema & Event Sourcing Logic)
* [ ] **Phase 3: The Brain** (Connecting LLM to `analyze_intent`)
* [ ] **Phase 4: The Loop** (Building the Interactive `[Y/n/e]` CLI)

```

---

