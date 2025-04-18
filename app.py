from completer import command_completer
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text import HTML

from rich.console import Console
from rich.table import Table

from scanner import run_scan
from scan_profiles import scan_profiles
from state import AppState
from utils import print_banner
from db import init_db, get_scan_history, get_scan_by_id

console = Console()

def print_help():
    table = Table(title="Available Commands", show_lines=True)
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")

    table.add_row("set target", "Set the target to scan (IP or domain)")
    table.add_row("set scan", "Select the scan type (from list)")
    table.add_row("show options", "Show currently selected target and scan")
    table.add_row("run", "Execute the configured scan")
    table.add_row("history", "Show saved scan history")
    table.add_row("view_result <id>", "View the output of a previous scan by ID")  
    table.add_row("help", "Show this help menu")
    table.add_row("exit / quit", "Exit the CLI tool")

    console.print(table)


def main():
    print_banner()
    init_db()
    state = AppState()

    # Setup prompt session for history, formatting, and completion
    session = PromptSession(
        completer=command_completer,
        history=InMemoryHistory()
    )

    while True:
        try:
            user_input = session.prompt(
                HTML("<cyan>nmapShell> </cyan>")
            ).strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[bold red]Use 'exit' or 'quit' to leave the shell.[/bold red]")
            continue

        if not user_input:
            continue  # Just press enter? Do nothing.

        if user_input.startswith("set target"):
            parts = user_input.split()
            if len(parts) >= 3:
                state.target = parts[2]
                console.print(f"[bold green]Target set to:[/bold green] {state.target}")
            else:
                console.print("[yellow]Please specify a target: e.g., set target 192.168.1.1[/yellow]")

        elif user_input == "set scan":
            console.print("[bold magenta]Available scan types:[/bold magenta]")
            scan_names = list(scan_profiles.keys())

            for i, name in enumerate(scan_names, 1):
                console.print(f"  [{i}] {name}")

            choice = session.prompt("Choose scan type (number): ").strip()

            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(scan_names):
                    selected = scan_names[index]
                    state.scan_type = selected
                    console.print(f"[green]Scan type set to:[/green] {selected}")
                else:
                    console.print("[red]Invalid number. Please choose from the list.[/red]")
            else:
                console.print("[red]Please enter a valid number.[/red]")


        elif user_input == "show options":
            console.print(f"\n[bold]Current Configuration:[/bold]")
            console.print(f"  [cyan]Target[/cyan]    : {state.target or '[not set]'}")
            console.print(f"  [cyan]Scan Type[/cyan] : {state.scan_type or '[not set]'}\n")

        elif user_input == "run":
            if not state.target or not state.scan_type:
                console.print("[red]You must set both a target and scan type before running.[/red]")
                continue

            scan_args = scan_profiles[state.scan_type]
            if state.scan_type == "Custom":
                custom = session.prompt("Enter custom nmap options: ")
                scan_args = custom.split()

            run_scan(state, scan_args)

        elif user_input == "history":
            history = get_scan_history()
            if not history:
                console.print("[dim]No scan history yet.[/dim]")
            else:
                table = Table(title="Scan History")
                table.add_column("ID", style="cyan")
                table.add_column("Target")
                table.add_column("Scan Type")
                table.add_column("Timestamp")
                for row in history:
                    table.add_row(str(row[0]), row[1], row[2], row[3])
                console.print(table)
        elif user_input.startswith("view_result"):
            parts = user_input.split()
            if len(parts) != 2 or not parts[1].isdigit():
                console.print("[red]Usage: view_result <id>[/red]")
                continue

            scan_id = int(parts[1])
            scan = get_scan_by_id(scan_id)
            if scan:
                console.print(f"\n[bold]Scan ID:[/bold] {scan[0]}")
                console.print(f"[bold]Target:[/bold] {scan[1]}")
                console.print(f"[bold]Scan Type:[/bold] {scan[2]}")
                console.print(f"[bold]Command:[/bold] {scan[3]}")
                console.print(f"[bold]Timestamp:[/bold] {scan[5]}")
                console.print("\n[bold green]Result:[/bold green]")
                console.print(scan[4])
            else:
                console.print(f"[red]No scan found with ID {scan_id}[/red]")
        elif user_input in ["exit", "quit"]:
            console.print("[bold green]Goodbye![/bold green]")
            break

        elif user_input == "help":
            print_help()

        else:
            console.print("[red]Unknown command. Type 'help' to see available commands.[/red]")


if __name__ == "__main__":
    main()
