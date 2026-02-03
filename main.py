import time
import yaml
import os
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text

from angel.voice import TheHerald, console
from angel.eyes import VisionSystem
from angel.wheels import Sephirot
from angel.halo import HaloSystem
from angel.brain import TheBrain
from angel.chronicles import TheScribe
from angel.types import AngelEvent, EdgeDef

# 1. Load the Holy Laws
with open("angel_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# 2. Awaken Modules
voice = TheHerald(name=config['angel_settings']['name'])
halo = HaloSystem(config)
wheels = Sephirot()
brain = TheBrain(config)
scribe = TheScribe("angel_chronicles.jsonl")

# 3. Rebuild state from chronicles on startup
read_limit = config.get("chronicles", {}).get("read_limit", 1000)
existing_events = scribe.read_all(limit=read_limit)
if existing_events:
    wheels.rebuild_from_chronicles(existing_events)
    voice.speak(
        f"Restored {len(existing_events)} recent events from the Chronicles.",
        style="angel.gold"
    )


def display_proposal(proposal):
    """Display the proposal in a beautiful table."""
    table = Table(title="Proposed Relationship", border_style="bright_magenta")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("File", proposal.edge.source)
    table.add_row("Intent", proposal.edge.target)
    table.add_row("Relationship", proposal.edge.edge_type)
    table.add_row("Confidence", f"{proposal.confidence:.0%}")
    table.add_row("Rationale", Text(proposal.rationale))
    if proposal.diff_summary:
        table.add_row("Changes", proposal.diff_summary)

    console.print(table)


def handle_change(file_path):
    """
    Triggered when the Eyes detect a file save.
    Now includes Human-in-the-Loop confirmation.
    """
    # A. Safety Check
    is_safe, msg = halo.check_safety()
    if not is_safe:
        voice.alert(f"HALO INTERVENTION: {msg}")
        return

    # B. Record the work unit
    filename = os.path.basename(file_path)
    voice.speak(f"I perceive a shift in: [u]{filename}[/u]", style="angel.gold")

    work_unit_event = AngelEvent(
        action_type="WORK_UNIT_CAPTURED",
        actor="AI_Agent",
        file_path=filename
    )
    scribe.record(work_unit_event)

    # C. The Brain analyzes intent
    proposal = brain.analyze_intent(file_path)

    proposal_event = AngelEvent(
        action_type="PROPOSAL_GENERATED",
        actor="AI_Agent",
        file_path=filename,
        proposal_id=proposal.proposal_id
    )
    scribe.record(proposal_event)

    # D. Present proposal for human confirmation
    console.print()
    display_proposal(proposal)
    console.print()

    # E. Human-in-the-Loop: Get confirmation (or auto-confirm)
    auto_confirm = config.get('brain', {}).get('auto_confirm', False)

    if auto_confirm:
        voice.speak("Auto-confirm enabled. Accepting proposal.", style="angel.gold")
        choice = "y"
    else:
        choice = Prompt.ask(
            "[bold magenta]Link this relationship?[/]",
            choices=["y", "n", "e"],
            default="y"
        )

    if choice == "y":
        # Confirmed - add to graph
        confirm_event = AngelEvent(
            action_type="PROPOSAL_CONFIRMED",
            actor="Human",
            file_path=filename,
            proposal_id=proposal.proposal_id,
            edge=proposal.edge,
            explicit_approval=True,
            justification=proposal.rationale
        )
        scribe.record(confirm_event)
        wheels.add_edge(proposal.edge)
        voice.speak("Relationship confirmed and recorded.", style="angel.pink")

    elif choice == "n":
        # Rejected
        reject_event = AngelEvent(
            action_type="PROPOSAL_REJECTED",
            actor="Human",
            file_path=filename,
            proposal_id=proposal.proposal_id,
            explicit_approval=False
        )
        scribe.record(reject_event)
        voice.speak("Proposal rejected. No changes made.", style="angel.gold")

    elif choice == "e":
        # Edit - provide custom intent
        custom_intent = Prompt.ask("[bold cyan]Enter your intent (2-4 words)[/]")
        if custom_intent.strip():
            custom_edge = EdgeDef(
                source=filename,
                target=custom_intent.strip(),
                edge_type="implements"
            )
            confirm_event = AngelEvent(
                action_type="PROPOSAL_CONFIRMED",
                actor="Human",
                file_path=filename,
                proposal_id=proposal.proposal_id,
                edge=custom_edge,
                explicit_approval=True,
                justification=f"Human override: {custom_intent}"
            )
            scribe.record(confirm_event)
            wheels.add_edge(custom_edge)
            voice.speak(f"Custom relationship recorded: {filename} → {custom_intent}", style="angel.pink")

    # F. Update visualization
    map_file = wheels.manifest()
    stats = wheels.get_stats()
    voice.speak(
        f"Constellation updated: {stats['files']} files, {stats['intents']} intents, {stats['edges']} links",
        style="angel.pink"
    )


def main():
    auto_confirm = config.get('brain', {}).get('auto_confirm', False)
    mode_text = "AUTO-CONFIRM MODE" if auto_confirm else "[Y]es / [N]o / [E]dit to respond"

    voice.proclaim(
        "BE NOT AFRAID",
        f"Python Accurate Angel v{config['angel_settings']['version']} is hovering.\n"
        f"Watching: {os.path.abspath(config['vision']['watch_path'])}\n"
        f"{mode_text}"
    )

    # Show existing graph stats
    stats = wheels.get_stats()
    if stats['total_nodes'] > 0:
        voice.speak(
            f"Current constellation: {stats['files']} files, {stats['intents']} intents",
            style="angel.gold"
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
            # Periodic Safety Check
            is_safe, msg = halo.check_safety()
            if not is_safe:
                voice.alert(f"SHUTTING DOWN: {msg}")
                break
    except KeyboardInterrupt:
        voice.speak("\nReturning to the ether...", style="angel.pink")
    finally:
        eyes.close_eyes()
        # Final stats
        stats = wheels.get_stats()
        voice.speak(
            f"Final constellation: {stats['files']} files, {stats['intents']} intents, {stats['edges']} links",
            style="angel.gold"
        )


if __name__ == "__main__":
    main()
