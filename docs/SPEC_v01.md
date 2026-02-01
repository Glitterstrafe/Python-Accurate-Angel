
---

# Project Specification: Python Accurate Angel (PAA)

**Version:** 1.0 (MVP)
**Concept:** An "AI-first" project observer that tracks code changes, visualizes relationships, and maintains project context using a "Biblically Accurate" aesthetic (Pink/Gold/Black).

## 1. File Structure

Create a root folder named `PythonAccurateAngel` with this hierarchy:

```text
PythonAccurateAngel/
├── angel_config.yaml       # Configuration & Theme
├── main.py                 # Entry Point
├── requirements.txt        # Dependencies
└── angel/                  # The Divine Modules
    ├── __init__.py         # (Empty file)
    ├── eyes.py             # File Watcher logic
    ├── voice.py            # UI & Terminal output
    ├── wheels.py           # Knowledge Graph generator
    └── halo.py             # Safety & Budget controls

```

---

## 2. Dependencies

**File:** `requirements.txt`

```text
watchdog==4.0.0
rich==13.7.0
networkx==3.2.1
pyvis==0.3.2
pyyaml==6.0.1

```

*Install command:* `pip install -r requirements.txt`

---

## 3. Configuration

**File:** `angel_config.yaml`

```yaml
angel_settings:
  name: "Ophanim-01"
  version: "1.0.0"
  
theme:
  # The "Biblically Cute" Palette
  primary: "#FF69B4"    # Hot Pink (The Mind)
  secondary: "#FFD700"  # Gold (The Glory)
  background: "#000000" # Void Black
  alert: "#FF1493"      # Deep Pink (Errors)
  text: "#FFFFFF"       # Starlight White

vision:
  watch_path: "./"      # The folder to watch (defaults to current)
  debounce_seconds: 2.0 # Time to wait after typing stops
  ignore_patterns:
    - "*.git*"
    - "*__pycache__*"
    - "*.env"
    - "*.DS_Store"
    - "*.html"          # Essential: Don't watch the graph itself or you get a loop!

halo:
  max_daily_cost_usd: 1.00
  emergency_stop_file: "STOP_ANGEL" # Create this file to kill the process

```

---

## 4. The Modules

### A. The Interface (UI)

**File:** `angel/voice.py`

```python
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text
from datetime import datetime

# Define the Theme
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
        """Standard speech (Pink)."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        console.print(f"[{timestamp}] [bold]{self.name}:[/] {message}", style=style)

    def proclaim(self, title, content):
        """Major updates (Gold Panel)."""
        text = Text(content, justify="center", style="black")
        panel = Panel(
            text, 
            title=f"[bold #000000]{title}[/]", 
            border_style="angel.gold",
            style="on #FF69B4", # Pink background
            padding=(1, 2)
        )
        console.print(panel)

    def alert(self, message):
        """Errors or Warnings."""
        console.print(f"👁️‍🗨️ [bold red]ALERT:[/] {message}", style="angel.gold")

```

### B. The Visual Graph

**File:** `angel/wheels.py`

```python
import networkx as nx
from pyvis.network import Network
import os

class Sephirot:
    """
    The Knowledge Graph. Tracks the lineage of code.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        # Theme colors
        self.c_agent = "#FF69B4" # Pink
        self.c_file = "#FFD700"  # Gold
        self.c_edge = "#FFFFFF"  # White

    def add_event(self, agent_thought, affected_file):
        """
        Links a thought (Pink) to a file (Gold).
        """
        # 1. Create a unique ID for the thought
        thought_id = f"Thought_{len(self.graph.nodes)}"
        
        # 2. Add the Thought Node
        self.graph.add_node(
            thought_id, 
            label="Agent Action", 
            title=agent_thought, # Tooltip shows details
            color=self.c_agent,
            shape="dot",
            size=15
        )

        # 3. Add the File Node (if it doesn't exist)
        if affected_file not in self.graph:
            self.graph.add_node(
                affected_file, 
                label=affected_file, 
                color=self.c_file, 
                shape="square",
                size=25
            )
            
        # 4. Link them
        self.graph.add_edge(thought_id, affected_file, color=self.c_edge)

    def manifest(self, output_file="angel_traceability.html"):
        """Generates the interactive HTML."""
        net = Network(height="750px", width="100%", bgcolor="#000000", font_color="white")
        
        # Convert NetworkX graph to Pyvis
        net.from_nx(self.graph)
        
        # Physics options for "floaty space" feel
        net.force_atlas_2based(
            gravity=-50, 
            central_gravity=0.01, 
            spring_length=100, 
            spring_strength=0.08
        )
        
        net.save_graph(output_file)
        return output_file

```

### C. The Watcher (Input)

**File:** `angel/eyes.py`

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Timer

class TheAllSeeingEye(FileSystemEventHandler):
    def __init__(self, callback, debounce_interval=2.0, ignore_patterns=None):
        self.callback = callback
        self.debounce_interval = debounce_interval
        self.ignore_patterns = ignore_patterns or []
        self.timer = None
        self.last_event_path = None

    def _is_ignored(self, path):
        for pattern in self.ignore_patterns:
            clean_pattern = pattern.replace("*", "")
            if clean_pattern in path:
                return True
        return False

    def _process_event(self):
        """Trigger the callback after silence."""
        if self.last_event_path:
            self.callback(self.last_event_path)

    def on_modified(self, event):
        if event.is_directory or self._is_ignored(event.src_path):
            return
        
        # Reset timer on new keystroke
        if self.timer:
            self.timer.cancel()
        
        self.last_event_path = event.src_path
        self.timer = Timer(self.debounce_interval, self._process_event)
        self.timer.start()

class VisionSystem:
    def __init__(self, path, callback, config):
        self.observer = Observer()
        self.handler = TheAllSeeingEye(
            callback, 
            config['vision']['debounce_seconds'],
            config['vision']['ignore_patterns']
        )
        self.path = path
    
    def open_eyes(self):
        self.observer.schedule(self.handler, self.path, recursive=True)
        self.observer.start()

    def close_eyes(self):
        self.observer.stop()
        self.observer.join()

```

### D. Safety Systems

**File:** `angel/halo.py`

```python
import os

class HaloSystem:
    def __init__(self, config):
        self.max_cost = config['halo']['max_daily_cost_usd']
        self.stop_file = config['halo']['emergency_stop_file']
        self.current_spend = 0.0

    def check_safety(self):
        """Returns (False, Reason) if safety is breached."""
        if os.path.exists(self.stop_file):
            return False, "Emergency Stop File Detected!"
        
        if self.current_spend >= self.max_cost:
            return False, "Mana Pool Depleted (Budget Limit Reached)"
            
        return True, "Systems Normal"

    def record_spend(self, cost):
        self.current_spend += cost

```

---

## 5. Main Application

**File:** `main.py`

```python
import time
import yaml
import os
from angel.voice import TheHerald
from angel.eyes import VisionSystem
from angel.wheels import Sephirot
from angel.halo import HaloSystem

# 1. Load the Holy Laws
with open("angel_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# 2. Awaken Modules
voice = TheHerald(name=config['angel_settings']['name'])
halo = HaloSystem(config)
wheels = Sephirot()

def handle_change(file_path):
    """
    Triggered when the Eyes detect a file save.
    """
    # A. Safety Check
    is_safe, msg = halo.check_safety()
    if not is_safe:
        voice.alert(f"HALO INTERVENTION: {msg}")
        return

    # B. The Angel Speaks
    filename = os.path.basename(file_path)
    voice.speak(f"I perceive a shift in: [u]{filename}[/u]", style="angel.gold")
    
    # C. SIMULATION: The Angel "Thinks" (Mock LLM)
    thought = f"Detected modification in {filename}. Updating internal logic..."
    
    # D. Update the Graph
    wheels.add_event(thought, filename)
    map_file = wheels.manifest()
    
    voice.speak(f"Constellation updated. View at: [link=file://{os.path.abspath(map_file)}]{map_file}[/link]", style="angel.pink")

def main():
    voice.proclaim(
        "BE NOT AFRAID", 
        f"Python Accurate Angel v{config['angel_settings']['version']} is hovering.\n"
        f"Watching: {os.path.abspath(config['vision']['watch_path'])}"
    )

    # Initialize Eyes
    eyes = VisionSystem(
        path=config['vision']['watch_path'], 
        callback=handle_change,
        config=config
    )

    eyes.open_eyes()

    try:
        while True:
            time.sleep(1)
            # Periodic Heartbeat / Safety Check
            is_safe, msg = halo.check_safety()
            if not is_safe:
                voice.alert(f"SHUTTING DOWN: {msg}")
                break
    except KeyboardInterrupt:
        voice.speak("\nReturning to the ether...", style="angel.pink")
    finally:
        eyes.close_eyes()

if __name__ == "__main__":
    main()

```

---

## 6. How to Run

1. Open your terminal.
2. Navigate to the `PythonAccurateAngel` directory.
3. Run: `python main.py`
4. Edit any file in the directory (save it) to trigger the Angel.
5. Open `angel_traceability.html` in your browser to see the live graph.
