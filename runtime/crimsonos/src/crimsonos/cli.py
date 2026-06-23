"""
Crimson OS CLI entry point (SCAFFOLDING demo).
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

BANNER = """
   ██████╗██████╗ ██╗███╗   ███╗███████╗ ██████╗ ███╗   ██╗     ██████╗ ███████╗
  ██╔════╝██╔══██╗██║████╗ ████║██╔════╝██╔═══██╗████╗  ██║    ██╔═══██╗██╔════╝
  ██║     ██████╔╝██║██╔████╔██║███████╗██║   ██║██╔██╗ ██║    ██║   ██║███████╗
  ██║     ██╔══██╗██║██║╚██╔╝██║╚════██║██║   ██║██║╚██╗██║    ██║   ██║╚════██║
  ╚██████╗██║  ██║██║██║ ╚═╝ ██║███████║╚██████╔╝██║ ╚████║    ╚██████╔╝███████║
   ╚═════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝     ╚═════╝ ╚══════╝

  Protocol Scaffold — SCAFFOLDING
  Crimson Symphony Media · Las Vegas, NV · 2026
"""


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("--help", "-h", "help"):
        _print_help()
        return

    command = args[0]

    if command == "status":
        _print_status()
    elif command == "dispatch":
        _dispatch_interactive()
    elif command == "ig":
        _ig_interactive()
    elif command == "run":
        _run_task()
    elif command == "version":
        from crimsonos import __version__
        console.print(f"crimsonos v{__version__}")
    else:
        console.print(f"[red]Unknown command: {command}[/red]")
        console.print("Run [bold]crimsonos --help[/bold] for usage.")
        sys.exit(1)


def _print_help():
    console.print(BANNER, style="bold red")
    table = Table(show_header=True, header_style="bold")
    table.add_column("Command")
    table.add_column("Description")
    table.add_row("status", "Show scaffold routing table (target topology)")
    table.add_row("dispatch", "Route a task through the dispatcher interactively")
    table.add_row("ig", "Run an IG audit on agent output")
    table.add_row("version", "Show version")
    console.print(Panel(table, title="Crimson OS CLI", border_style="red"))


def _print_status():
    from crimsonos.dispatcher import Dispatcher
    d = Dispatcher()
    console.print(d.status_table())


def _dispatch_interactive():
    console.print("[bold red]Crimson OS Dispatcher[/bold red]")
    content = console.input("[cyan]Task:[/cyan] ")
    mode = console.input("[cyan]Operator mode (entrepreneur/architect/worship/etc):[/cyan] ").strip()

    from crimsonos.dispatcher import Dispatcher
    from crimsonos.super_token import LogosToken
    d = Dispatcher()
    token = LogosToken(content=content, context={"operator_mode": mode or "architect"})
    result = d.route(token)
    console.print(Panel(str(result), title="Dispatcher Output", border_style="green"))


def _ig_interactive():
    console.print("[bold red]Crimson OS IG Protocol[/bold red]")
    agent_name = console.input("[cyan]Agent name:[/cyan] ").strip()
    output = console.input("[cyan]Agent output to audit:[/cyan] ").strip()
    self_score = float(console.input("[cyan]Agent self-reported score (0-10):[/cyan] ").strip() or "0")

    from crimsonos.ig import IGProtocol
    ig = IGProtocol()
    result = ig.audit(agent_name=agent_name, output=output, self_reported_score=self_score)
    console.print(Panel(str(result), title="IG Audit Result", border_style="yellow"))


if __name__ == "__main__":
    main()


def _run_task():
    """Full pipeline: dispatch + execute via NEO Ollama."""
    import os
    console.print("[bold red]Crimson OS — Dispatch + Execute[/bold red]")
    console.print(f"[dim]Ollama: {os.getenv('OLLAMA_BASE', 'http://192.168.1.156:11434')} | Model: {os.getenv('DEFAULT_MODEL', 'deepseek-r1:7b')}[/dim]")

    content = console.input("[cyan]Task:[/cyan] ").strip()
    if not content:
        return

    from crimsonos.dispatcher import Dispatcher
    from crimsonos.super_token import SuperToken, TokenType
    from crimsonos.executor import execute

    d = Dispatcher()
    token = SuperToken(content=content, token_type=TokenType.LOGOS)
    result = d.route(token)

    console.print(f"[yellow]→ Track {result.track.value} | Agents: {', '.join(result.assigned_agents)}[/yellow]")
    console.print("[dim]Calling NEO...[/dim]")

    response = execute(result, content)
    from rich.panel import Panel
    console.print(Panel(response, title=f"NEO via {result.assigned_agents[0]}", border_style="green"))
