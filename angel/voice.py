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
            style="on #FF69B4",  # Pink background
            padding=(1, 2)
        )
        console.print(panel)

    def alert(self, message):
        """Errors or Warnings."""
        console.print(f"[bold red]ALERT:[/] {message}", style="angel.gold")
