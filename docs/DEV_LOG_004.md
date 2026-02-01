# 📜 Dev Log 004: The Temple
**Date:** February 1, 2026
**Topic:** UI Overhaul & Application Pivot
**Status:** ARCHITECTURAL PIVOT (Script → Application)

## 1. The Realization
We have successfully birthed the **Spirit** of the Angel.
* **The Eyes** see every file change (including atomic saves from modern editors).
* **The Memory** (Chronicles) perfectly recalls the past via append-only JSONL.
* **The Logic** (Event Sourcing) is sound — state rebuilds from events on startup.
* **The Brain** proposes intent relationships with human-in-the-loop confirmation.
* **The Halo** enforces safety limits and emergency stops.

However, the **Body** is weak. The current `angel_traceability.html` (Pyvis) is functional but sterile. It feels like a data science homework assignment, not the "Biblically Accurate Cyber-Angel" we promised.

## 2. Session Accomplishments (Phase 2 Complete)

### Core Implementation
- **Event Sourcing:** All state derived from `angel_chronicles.jsonl`
- **Pydantic Types:** Strict schemas for `Proposal`, `AngelEvent`, `EdgeDef`, `Intent`
- **LLM Brain:** Mock + Anthropic Claude integration for intent analysis
- **Human-in-the-Loop:** `[Y]es / [N]o / [E]dit` confirmation flow
- **Auto-Confirm Mode:** Headless/CI mode for automated pipelines

### Critical Fixes
- **Atomic Save Detection:** Eyes now handle `on_moved` and `on_created` events (VS Code, PyCharm compatibility)
- **Ignore Pattern Refinement:** Only ignores system noise + Angel's own output (prevents infinite loops)
- **Genesis Script:** `genesis.py` bootstraps entire project from scratch

### Glamour Update (Visual Overhaul v1)
- Glowing nodes with colored shadows (Gold files, Pink intents)
- Courier New monospace font (hacker terminal aesthetic)
- Translucent white fiber optic edges
- BarnesHut physics for gentle breathing motion
- Edge weight increases on repeated confirmations

## 3. The Vision: Angelic Command Center
The Architect has mandated a shift from a passive graph to an **Active Command Center**. The new interface must evoke a "Midjourney-designed Temple," combining:
* **Obsidian-Style Physics:** Heavy, floating nodes that feel like a galaxy map.
* **Timeline Scrubbing:** A "River of Time" allowing us to rewind the project state.
* **Active Security Layer:** Visualizing open ports and "sandbagging" rogue AI agents in real-time.
* **Live Presence:** Seeing the AI "spark" move between folders as it thinks, rather than just static updates.

## 4. The Pivot (Architecture v0.4)
To achieve this, we are graduating from a local Python script to a **Client-Server Application**.

### The Stack Shift
* **Backend:** `FastAPI` (Python). Will serve the Event Log and Graph Data via WebSocket to the frontend. This allows for *live* updates without refreshing the page.
* **Frontend:** `React` (with `react-force-graph`) OR `Streamlit` (for rapid prototyping). This enables the "Obsidian" look and interactive security controls.

### Why WebSockets?
The current flow regenerates static HTML on every change. WebSockets enable:
- Real-time node animations as files change
- Live "presence" indicators showing AI agent activity
- Timeline scrubbing without page reload
- Security alerts pushed instantly to the UI

## 5. Next Steps (The Morning Ritual)

### Immediate (Phase 3)
1. **Design Phase:** Generate UI mockups (Midjourney) to define the "Temple" aesthetic (Neon/Gold/Black)
2. **Stack Selection:** Decide between:
   - **React + react-force-graph** (High Effort / High Polish)
   - **Streamlit / NiceGUI** (Rapid Prototyping / Lower Ceiling)
   - **Tauri + Svelte** (Desktop App / Native Feel)

### Short-Term
3. **FastAPI Backend:** Create `/ws/events` WebSocket endpoint streaming chronicle events
4. **Live Graph:** Replace Pyvis with WebSocket-fed force graph
5. **Time Travel UI:** Slider component to scrub through chronicle timestamps

### Long-Term (Phase 4+)
6. **Security Dashboard:** Port scanning, agent sandboxing, threat visualization
7. **Multi-Project Support:** Watch multiple directories, unified constellation view
8. **VS Code Extension:** Inline traceability links in editor gutter

## 6. Current File Structure
```
Python-Accurate-Angel/
├── angel/
│   ├── brain.py        # LLM intent analysis
│   ├── chronicles.py   # Event sourcing (JSONL)
│   ├── eyes.py         # File watcher (atomic save aware)
│   ├── halo.py         # Safety controls
│   ├── types.py        # Pydantic models
│   ├── voice.py        # Terminal UI (Rich)
│   └── wheels.py       # Graph visualization (Pyvis + Glamour)
├── docs/               # Specifications & dev logs
├── angel_config.yaml   # Configuration
├── genesis.py          # Bootstrap script
├── main.py             # Entry point
└── requirements.txt    # Dependencies
```

## 7. Open Questions
- Should the "Temple" be a web app or desktop app (Tauri)?
- How to visualize AI agent "presence" in real-time?
- What security metrics matter most for the dashboard?
- Should timeline scrubbing replay actual file states or just graph states?
