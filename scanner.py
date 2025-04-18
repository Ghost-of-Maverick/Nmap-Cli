import subprocess
from rich.console import Console
from db import save_scan

console = Console()

def run_scan(state, scan_args):
    if not state.target or not state.scan_type:
        console.print("[red]Target and scan type must be set before running scan.[/red]")
        return

    cmd = ["nmap"] + scan_args + [state.target]
    command_str = " ".join(cmd)
    console.print(f"[cyan]Running: {command_str}[/cyan]")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        console.print(f"[green]{output}[/green]")
        save_scan(state.target, state.scan_type, command_str, output)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Scan failed: {e.stderr}[/red]")
