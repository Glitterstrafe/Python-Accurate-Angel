
```markdown
# 👁️ Python Accurate Angel (PAA)

> *"Be Not Afraid."*

**Python Accurate Angel** is an "AI-first" project observer designed to bring "Biblically Accurate" omniscience to your local development environment. It tracks code changes in real-time, visualizes the hidden relationships between your files, and maintains a living context of your project's evolution.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Aesthetic](https://img.shields.io/badge/Aesthetic-Pink%2FGold%2FBlack-ff69b4)

## ✨ Features

* **The Eyes (File Watcher):** Automatically detects changes in your project with smart debouncing (doesn't trigger while you type).
* **The Voice (Interface):** A beautiful `rich` terminal interface using a **Pink/Gold/Black** aesthetic.
* **The Wheels (Knowledge Graph):** Generates an interactive, physics-based HTML graph (`angel_traceability.html`) showing how your code files connect to AI "thoughts."
* **The Halo (Safety):** Built-in kill switches and budget limiters to prevent runaway AI loops.

---

## 🚀 Quick Start

### 1. Installation

Clone this repository and install the required "offerings" (dependencies):

```bash
git clone [https://github.com/YOUR_USERNAME/PythonAccurateAngel.git](https://github.com/YOUR_USERNAME/PythonAccurateAngel.git)
cd PythonAccurateAngel
pip install -r requirements.txt

```

### 2. Configuration (`angel_config.yaml`)

The system is pre-configured with the "Ophanim-01" personality. You can adjust the **Safety Halo** or **Watch Paths** in `angel_config.yaml`.

### 3. Summon the Angel

Run the main script to start the observer:

```bash
python main.py

```

* **Trigger:** Edit and save any file in the directory.
* **Observe:** Watch the terminal for Gold/Pink updates.
* **Visualize:** Open `angel_traceability.html` in your browser to see the living graph.

---

## 📂 Project Architecture

If you are building this from scratch, here is the required structure:

```text
PythonAccurateAngel/
├── angel_config.yaml       # Configuration & Theme
├── main.py                 # Entry Point
├── requirements.txt        # Dependencies
└── angel/                  # The Divine Modules
    ├── __init__.py         # (Empty)
    ├── eyes.py             # Watchdog Logic
    ├── voice.py            # Rich UI Wrapper
    ├── wheels.py           # NetworkX/Pyvis Graph Generator
    └── halo.py             # Safety & Budget Logic

```

---

## 📜 The Code Specification

### `angel/voice.py` (The Interface)

```python
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text
from datetime import datetime

angel_theme = Theme({
    "angel.pink": "#FF69B4",
    "angel.gold": "#FFD700",
    "angel.alert": "bold red on #FFD700"
})
console = Console(theme=angel_theme)

class TheHerald:
    def __init__(self, name="Angel"):
        self.name = name
    def speak(self, message, style="angel.pink"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        console.print(f"[{timestamp}] [bold]{self.name}:[/] {message}", style=style)
    def proclaim(self, title, content):
        text = Text(content, justify="center", style="black")
        panel = Panel(text, title=f"[bold #000000]{title}[/]", border_style="angel.gold", style="on #FF69B4", padding=(1, 2))
        console.print(panel)
    def alert(self, message):
        console.print(f"👁️‍🗨️ [bold red]ALERT:[/] {message}", style="angel.gold")

```

### `angel/wheels.py` (The Graph)

```python
import networkx as nx
from pyvis.network import Network

class Sephirot:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.c_agent = "#FF69B4"
        self.c_file = "#FFD700"
        self.c_edge = "#FFFFFF"

    def add_event(self, agent_thought, affected_file):
        thought_id = f"Thought_{len(self.graph.nodes)}"
        self.graph.add_node(thought_id, label="Agent Action", title=agent_thought, color=self.c_agent, shape="dot", size=15)
        if affected_file not in self.graph:
            self.graph.add_node(affected_file, label=affected_file, color=self.c_file, shape="square", size=25)
        self.graph.add_edge(thought_id, affected_file, color=self.c_edge)

    def manifest(self, output_file="angel_traceability.html"):
        net = Network(height="750px", width="100%", bgcolor="#000000", font_color="white")
        net.from_nx(self.graph)
        net.force_atlas_2based(gravity=-50, central_gravity=0.01, spring_length=100, spring_strength=0.08)
        net.save_graph(output_file)
        return output_file

```

*(Note: Full source code for `eyes.py`, `halo.py`, and `main.py` is included in the repo source files.)*

```

### One Final Detail: `.gitignore`
Before you commit, make sure you create a file named `.gitignore` in the root folder and add this to it. This prevents you from accidentally uploading the graph itself or your virtual environment settings:

```text
__pycache__/
*.pyc
.env
.DS_Store
angel_traceability.html
venv/

```

Would you like me to whip up a quick "logo" description you can put in the repo, or are you good to go?
