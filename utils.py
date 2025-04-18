from rich.panel import Panel
from rich.console import Console

def print_banner():
    banner = """[bold cyan]
     _   _                          _____ _          _ _ 
    | \ | |                        / ____| |        | | |
    |  \| | _____      _____ _ __ | (___ | |__   ___| | |
    | . ` |/ _ \ \ /\ / / _ \ '__| \___ \| '_ \ / _ \ | |
    | |\  |  __/\ V  V /  __/ |    ____) | | | |  __/ | |
    |_| \_|\___| \_/\_/ \___|_|   |_____/|_| |_|\___|_|_|
    
    [green]NmapShell - Powerful CLI Port Scanner[/green]
    [/bold cyan]"""
    Console().print(Panel(banner, expand=False, style="bold green"))

