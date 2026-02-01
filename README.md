
```markdown
# 👁️ Python Accurate Angel (PAA)

> *"Be Not Afraid. Be Traceable."*

**Python Accurate Angel** is an **AI-Native Traceability System** designed to capture intent, relationships, and temporal history as first-class artifacts. 

It wraps a rigorous engineering philosophy—**Event Sourcing** and **Explicit Relationships**. It watches your work, analyzes your intent, and maintains a living, physics-based graph of your project's evolution.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-0.2_Alpha-ff69b4)
![Architecture](https://img.shields.io/badge/Architecture-Event_Sourced-blue)

```text
      .   * .       
   * _ / \ _   * .
 .   /  o.o  \      *
    (  ( _ )  )   .  
   . \   |   /  * * \  |  /      . 
   .   \ | /   * * \|/  .       
         V           
 BE  NOT  AFRAID     

```

---

## 📐 The Vision: AI-Native Traceability

Traditional tools force you to reconstruct "why" a change happened months after the fact (the "Context Reconstruction Tax"). PAA prepays this tax by capturing the context *while* you work.

### Core Principles

1. **Explicit over Inferred:** The AI does not guess. It *proposes* relationships ("Is this a jitter fix?"), and the Human *confirms*. This prevents the Knowledge Graph from being corrupted by hallucinations.
2. **Event-Sourced Truth:** The "Truth" of the project is not just the current code, but the immutable log of every thought, decision, and link that led here.
3. **Context as Infrastructure:** Traceability is not a document you write at the end. It is a graph that grows alongside your code.

---

## ✨ System Architecture

The system is composed of five distinct "Divine Modules":

### 1. The Eyes (Observation Layer)

* **Role:** Passive File Watching.
* **Tech:** `watchdog` with intelligent debouncing.
* **Function:** Detects "Work Units" (saves) and filters out noise (`.git`, `__pycache__`) so the system only reacts to meaningful intent.

### 2. The Brain (Logic Core)

* **Role:** Analysis & Proposal.
* **Tech:** LLM Integration (OpenAI/Gemini/Claude).
* **Function:** Analyzes the `git diff`, determines the likely intent, and **proposes** a link to the Knowledge Graph for human approval.

### 3. The Wheels (Relationship Map)

* **Role:** Visualization.
* **Tech:** `NetworkX` & `Pyvis`.
* **Function:** Generates an interactive, physics-based HTML graph (`angel_traceability.html`) showing the constellation of Files, Agents, and Decisions.

### 4. The Chronicles (Event Log)

* **Role:** Immutable History.
* **Tech:** JSON Event Sourcing.
* **Function:** Stores the sequence of all graph mutations, enabling "Time Travel" (replay) of the project's history.

### 5. The Halo (Safety Controls)

* **Role:** Operational Safety.
* **Tech:** Budget Limiters & Kill Switches.
* **Function:** Enforces a "Mana Pool" (daily cost limit) and monitors for an emergency stop file to prevent AI loops.

---

## 🚀 Quick Start

### 1. Installation

Clone the repository and install the "offerings" (dependencies):

```bash
git clone [https://github.com/YOUR_USERNAME/PythonAccurateAngel.git](https://github.com/YOUR_USERNAME/PythonAccurateAngel.git)
cd PythonAccurateAngel
pip install -r requirements.txt

```

### 2. Configuration (`angel_config.yaml`)

The system uses a YAML file to control the "Ophanim-01" personality and safety settings.

```yaml
angel_settings:
  name: "Ophanim-01"
theme:
  primary: "#FF69B4" # Hot Pink
  secondary: "#FFD700" # Gold
halo:
  max_daily_cost_usd: 1.00

```

### 3. Summon the Angel

Run the main script to start the observer:

```bash
python main.py

```

* **Trigger:** Edit and save any file in the directory.
* **Observe:** The terminal will notify you of the detected shift in the "Ether."
* **Visualize:** Open `angel_traceability.html` in your browser to see the living graph.

---

## 🗺️ Roadmap

* **Phase 1 (Complete):** File Watching, Visual Graph Generation, Safety Halo.
* **Phase 2 (In Progress):** "Human-in-the-Loop" Confirmation Protocol (The `Y/N` Terminal Flow).
* **Phase 3:** Connecting the "Brain" (LLM API) for intent analysis.
* **Phase 4:** Temporal Replay (Time Travel view of the graph).

---
## 🤝 Acknowledgments
Inspiration:
* **Brock Webb** – *Architectural Vision & Inspiration*
    * For the original inspiring linkedin post asking if this could/should be built and for "AI-Native Traceability" specification that defines the logical core and epistemology of this system. The "Explicit Truth" and "Event Sourcing" philosophies are derived from his foundational work.
---

## 📜 License

**MIT License** - Free to use, fork, and build upon. The Angel watches all.

```

```
