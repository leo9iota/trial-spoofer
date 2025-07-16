#!/usr/bin/env python3
"""
ULTIMATE TEXTUAL & RICH DEMO
A comprehensive showcase of all Textual and Rich features.
Designed to look like something from hacker movies with a dark, terminal aesthetic.
"""

from __future__ import annotations

import asyncio
import random

from rich.json import JSON
from rich.layout import Layout
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.widgets import (
    Button,
    Checkbox,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Log,
    ProgressBar,
    RadioButton,
    RadioSet,
    Select,
    Sparkline,
    Static,
    Switch,
    TabbedContent,
    TabPane,
    TextArea,
)
from textual.widgets import (
    Markdown as TextualMarkdown,
)
from textual.widgets import (
    Tree as TextualTree,
)


class RichShowcase(Static):
    """Widget to showcase Rich features."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.demo_index = 0
        self.demos = [
            self.create_text_demo,
            self.create_table_demo,
            self.create_progress_demo,
            self.create_tree_demo,
            self.create_syntax_demo,
            self.create_json_demo,
            self.create_markdown_demo,
            self.create_layout_demo,
        ]

    def create_text_demo(self) -> Panel:
        """Demonstrate Rich text styling."""
        text = Text()
        text.append("Rich Text Styling Demo\n\n", style="bold magenta")
        text.append("Bold ", style="bold")
        text.append("Italic ", style="italic")
        text.append("Underline ", style="underline")
        text.append("Strike ", style="strike")
        text.append("Blink\n", style="blink")
        text.append("Colors: ", style="white")
        text.append("Red ", style="red")
        text.append("Green ", style="green")
        text.append("Blue ", style="blue")
        text.append("Yellow ", style="yellow")
        text.append("Magenta ", style="magenta")
        text.append("Cyan\n", style="cyan")
        text.append("Background: ", style="white")
        text.append("Red BG ", style="white on red")
        text.append("Blue BG ", style="white on blue")
        text.append("Green BG\n", style="black on green")
        text.append("🎉 Emoji support: 🚀 🔥 ⭐ 💎 🎯", style="bold")

        return Panel(
            text, title="[bold cyan]Rich Text Features[/bold cyan]", border_style="cyan"
        )

    def create_table_demo(self) -> Panel:
        """Demonstrate Rich tables."""
        table = Table(
            title="🛡️ Security Features", show_header=True, header_style="bold magenta"
        )
        table.add_column("Feature", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Risk Level", justify="center")
        table.add_column("Status", justify="center")

        features = [
            ("MAC Spoofing", "Change network interface MAC", "🟢 Low", "✅ Active"),
            ("Machine ID", "Regenerate system machine-id", "🟢 Low", "⏳ Pending"),
            ("UUID Random", "Randomize filesystem UUID", "🟡 Medium", "❌ Failed"),
            ("Hostname", "Set random hostname", "🟢 Low", "✅ Active"),
            ("Cache Clean", "Purge editor caches", "🟢 Low", "✅ Active"),
        ]

        for feature, desc, risk, status in features:
            table.add_row(feature, desc, risk, status)

        return Panel(
            table, title="[bold green]Rich Tables[/bold green]", border_style="green"
        )

    def create_progress_demo(self) -> Panel:
        """Demonstrate Rich progress bars."""
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
        )

        task1 = progress.add_task("Downloading...", total=100)
        task2 = progress.add_task("Processing...", total=100)
        task3 = progress.add_task("Uploading...", total=100)

        progress.update(task1, completed=75)
        progress.update(task2, completed=45)
        progress.update(task3, completed=90)

        return Panel(
            progress,
            title="[bold yellow]Rich Progress Bars[/bold yellow]",
            border_style="yellow",
        )

    def create_tree_demo(self) -> Panel:
        """Demonstrate Rich trees."""
        tree = Tree("📁 [bold blue]Project Structure[/bold blue]")

        src_branch = tree.add("📁 [cyan]src/[/cyan]")
        src_branch.add("📄 [green]main.py[/green]")
        src_branch.add("📄 [green]demo.py[/green]")
        src_branch.add("📄 [green]tui.py[/green]")

        utils_branch = src_branch.add("📁 [cyan]utils/[/cyan]")
        utils_branch.add("📄 [green]helper.py[/green]")
        utils_branch.add("📄 [green]spoofer.py[/green]")
        utils_branch.add("📄 [green]system.py[/green]")

        docs_branch = tree.add("📁 [cyan]docs/[/cyan]")
        docs_branch.add("📄 [blue]README.md[/blue]")
        docs_branch.add("📄 [blue]CHANGELOG.md[/blue]")

        return Panel(
            tree, title="[bold blue]Rich Trees[/bold blue]", border_style="blue"
        )

    def create_syntax_demo(self) -> Panel:
        """Demonstrate Rich syntax highlighting."""
        code = '''def hack_the_planet():
    """Elite hacker function."""
    import os
    import sys

    # Matrix-style code
    for i in range(10):
        print(f"Accessing mainframe... {i*10}%")
        time.sleep(0.1)

    return "Access granted!"

if __name__ == "__main__":
    result = hack_the_planet()
    print(f"Status: {result}")'''

        syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
        return Panel(
            syntax,
            title="[bold red]Rich Syntax Highlighting[/bold red]",
            border_style="red",
        )

    def create_json_demo(self) -> Panel:
        """Demonstrate Rich JSON rendering."""
        data = {
            "system": {
                "name": "HACKER_TERMINAL",
                "version": "2.0.0",
                "status": "ONLINE",
                "features": [
                    {"name": "Stealth Mode", "enabled": True},
                    {"name": "Encryption", "level": "AES-256"},
                    {"name": "Proxy Chain", "hops": 7},
                ],
                "targets": {
                    "primary": "192.168.1.1",
                    "secondary": "10.0.0.1",
                    "backup": "172.16.0.1",
                },
            }
        }

        json_render = JSON.from_data(data)
        return Panel(
            json_render,
            title="[bold magenta]Rich JSON[/bold magenta]",
            border_style="magenta",
        )

    def create_markdown_demo(self) -> Panel:
        """Demonstrate Rich markdown."""
        markdown_text = """
# Hacker Terminal v2.0

## Features
- **Stealth Mode**: Invisible to detection systems
- **Multi-layer Encryption**: Military-grade security
- **Real-time Monitoring**: Live system status

## Commands
1. `hack --target <ip>` - Initiate attack
2. `stealth --enable` - Activate stealth mode
3. `encrypt --level max` - Maximum encryption

> **Warning**: For educational purposes only!

```bash
$ ./hacker_terminal --mode stealth
[+] Stealth mode activated
[+] All traces erased
```
        """

        markdown = Markdown(markdown_text)
        return Panel(
            markdown,
            title="[bold white]Rich Markdown[/bold white]",
            border_style="white",
        )

    def create_layout_demo(self) -> Panel:
        """Demonstrate Rich layouts."""
        layout = Layout()
        layout.split_column(
            Layout(Panel("Header Section", style="bold blue"), name="header", size=3),
            Layout(name="body"),
            Layout(Panel("Footer Section", style="bold red"), name="footer", size=3),
        )

        layout["body"].split_row(
            Layout(Panel("Left Panel\nSidebar", style="green"), name="left"),
            Layout(Panel("Right Panel\nMain Content", style="yellow"), name="right"),
        )

        return Panel(
            layout, title="[bold cyan]Rich Layouts[/bold cyan]", border_style="cyan"
        )

    def next_demo(self) -> None:
        """Show next demo."""
        self.demo_index = (self.demo_index + 1) % len(self.demos)
        self.update(self.demos[self.demo_index]())

    def on_mount(self) -> None:
        """Initialize with first demo."""
        self.update(self.demos[0]())


class UltimateDemo(App):
    """Ultimate demonstration of Textual and Rich features."""

    CSS = """
    Screen {
        background: #000011;
    }

    .header {
        height: 3;
        background: #001122;
        color: #00ff00;
        border: solid #00ff00;
    }

    .main-container {
        height: 1fr;
        background: #000011;
    }

    .demo-panel {
        background: #000011;
        border: solid #00ffff;
        margin: 1;
    }

    .controls-panel {
        background: #000011;
        border: solid #ffff00;
        margin: 1;
        height: 1fr;
    }

    .log-panel {
        background: #000011;
        border: solid #ff00ff;
        margin: 1;
        height: 1fr;
    }

    Button {
        background: #001122;
        color: #00ff00;
        border: solid #00ff00;
        margin: 1;
    }

    Button:hover {
        background: #003300;
        color: #ffffff;
    }

    Input {
        background: #001122;
        color: #00ffff;
        border: solid #00ffff;
    }

    Select {
        background: #001122;
        color: #ffff00;
        border: solid #ffff00;
    }

    DataTable {
        background: #001122;
        color: #00ff00;
    }

    TextArea {
        background: #001122;
        color: #00ffff;
        border: solid #00ffff;
    }

    Log {
        background: #001122;
        color: #00ff00;
        border: solid #00ff00;
    }

    ProgressBar {
        color: #00ff00;
    }

    Switch {
        background: #001122;
    }

    Checkbox {
        background: #001122;
        color: #00ff00;
    }

    RadioButton {
        background: #001122;
        color: #00ff00;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.rich_showcase: RichShowcase | None = None
        self.demo_log: Log | None = None
        self.data_table: DataTable | None = None
        self.progress_bars: list[ProgressBar] = []
        self.sparkline_data = [random.randint(0, 100) for _ in range(50)]

    def compose(self) -> ComposeResult:
        """Create the comprehensive demo layout."""
        yield Header(show_clock=True)

        # Main tabbed interface
        with TabbedContent(initial="rich-demo"):
            # Rich Features Demo Tab
            with TabPane("Rich Features", id="rich-demo"):
                with Horizontal():
                    with Vertical(classes="demo-panel"):
                        self.rich_showcase = RichShowcase(id="rich-showcase")
                        yield self.rich_showcase
                        yield Button("Next Rich Demo", id="next-rich-btn")

                    with Vertical(classes="controls-panel"):
                        yield Static("[bold cyan]Rich Controls[/bold cyan]")
                        yield Button("Text Styling", id="text-demo")
                        yield Button("Tables", id="table-demo")
                        yield Button("Progress Bars", id="progress-demo")
                        yield Button("Trees", id="tree-demo")
                        yield Button("Syntax Highlighting", id="syntax-demo")
                        yield Button("JSON Rendering", id="json-demo")
                        yield Button("Markdown", id="markdown-demo")
                        yield Button("Layouts", id="layout-demo")

            # Textual Widgets Tab
            with TabPane("Textual Widgets", id="textual-demo"):
                with ScrollableContainer():
                    yield Static(
                        "[bold magenta]🎛️ TEXTUAL WIDGETS SHOWCASE[/bold magenta]"
                    )

                    # Input widgets section
                    yield Static("[bold cyan]📝 Input Widgets[/bold cyan]")
                    yield Input(placeholder="Type something here...", id="demo-input")
                    yield TextArea(
                        "Multi-line text area\nType your code here...",
                        id="demo-textarea",
                    )

                    # Selection widgets
                    yield Static("[bold cyan]🎯 Selection Widgets[/bold cyan]")
                    yield Select(
                        [
                            ("Option 1", "opt1"),
                            ("Option 2", "opt2"),
                            ("Option 3", "opt3"),
                        ],
                        id="demo-select",
                    )

                    with RadioSet(id="demo-radio"):
                        yield RadioButton("Radio Option 1", id="radio1")
                        yield RadioButton("Radio Option 2", id="radio2")
                        yield RadioButton("Radio Option 3", id="radio3")

                    yield Checkbox("Enable hacker mode", id="demo-checkbox")
                    yield Switch(value=True, id="demo-switch")

                    # Progress and data widgets
                    yield Static("[bold cyan]📊 Progress & Data Widgets[/bold cyan]")
                    yield ProgressBar(total=100, show_eta=True, id="demo-progress")
                    yield Sparkline(
                        [1, 2, 3, 5, 8, 13, 21, 34, 55, 89], id="demo-sparkline"
                    )

                    # Data table
                    self.data_table = DataTable(id="demo-datatable")
                    yield self.data_table

                    # List view
                    yield Static("[bold cyan]📋 List & Tree Widgets[/bold cyan]")
                    yield ListView(
                        ListItem(Label("🔥 Hack the mainframe")),
                        ListItem(Label("🚀 Launch cyber attack")),
                        ListItem(Label("🛡️ Enable stealth mode")),
                        ListItem(Label("💻 Access secure systems")),
                        id="demo-listview",
                    )

                    # Tree widget
                    yield TextualTree("🌐 Network Structure", id="demo-tree")

            # Interactive Demo Tab
            with TabPane("Interactive Demo", id="interactive-demo"):
                with Horizontal():
                    with Vertical(classes="controls-panel"):
                        yield Static(
                            "[bold yellow]🎮 Interactive Controls[/bold yellow]"
                        )
                        yield Button(
                            "🚀 Start Hacking", id="start-hack", variant="success"
                        )
                        yield Button(
                            "🛡️ Enable Stealth", id="stealth-mode", variant="warning"
                        )
                        yield Button(
                            "💥 Launch Attack", id="launch-attack", variant="error"
                        )
                        yield Button("🔄 Reset System", id="reset-system")
                        yield Button("📊 Generate Data", id="generate-data")
                        yield Button("🎲 Random Action", id="random-action")

                        yield Static("[bold cyan]System Status[/bold cyan]")
                        yield ProgressBar(total=100, id="system-health")
                        yield ProgressBar(total=100, id="stealth-level")
                        yield ProgressBar(total=100, id="attack-progress")

                    with Vertical(classes="log-panel"):
                        yield Static("[bold green]🖥️ System Log[/bold green]")
                        self.demo_log = Log(id="demo-log")
                        yield self.demo_log

            # Markdown Demo Tab
            with TabPane("Markdown Demo", id="markdown-tab"):
                markdown_content = """
# 🔥 ULTIMATE HACKER TERMINAL

## 🎯 Mission Objectives
- [x] Infiltrate target systems
- [x] Bypass security protocols
- [ ] Extract classified data
- [ ] Cover tracks and exit

## 🛠️ Available Tools

### Network Tools
- **Nmap**: Network discovery and security auditing
- **Wireshark**: Network protocol analyzer
- **Metasploit**: Penetration testing framework

### Exploitation Tools
- **Burp Suite**: Web application security testing
- **SQLmap**: Automatic SQL injection tool
- **John the Ripper**: Password cracking tool

## 📊 System Status

| Component | Status | Level |
|-----------|--------|-------|
| Firewall  | 🔴 Bypassed | 95% |
| Encryption| 🟡 Cracking | 67% |
| Stealth   | 🟢 Active   | 100% |

## 🚨 Security Alerts

> **WARNING**: Unauthorized access detected!
>
> All activities are being monitored for educational purposes only.

## 💻 Code Example

```python
def hack_mainframe():
    print("Accessing mainframe...")
    for i in range(100):
        print(f"Progress: {i}%")
    print("Access granted!")
```

## 🌐 Network Map

```
Internet
├── Router (192.168.1.1)
├── Firewall (192.168.1.2)
├── DMZ
│   ├── Web Server (192.168.1.10)
│   └── Mail Server (192.168.1.11)
└── Internal Network
    ├── Database (10.0.0.5)
    ├── File Server (10.0.0.6)
    └── Workstations (10.0.0.10-50)
```

---

*Remember: With great power comes great responsibility!*
                """
                yield TextualMarkdown(markdown_content, id="demo-markdown")

        yield Footer()

    def on_mount(self) -> None:
        """Initialize the application."""
        # Setup data table
        if self.data_table:
            self.data_table.add_columns("Target", "Status", "Progress", "Risk Level")
            self.data_table.add_row("192.168.1.1", "🔴 Compromised", "100%", "🟢 Low")
            self.data_table.add_row("10.0.0.5", "🟡 Scanning", "67%", "🟡 Medium")
            self.data_table.add_row("172.16.0.1", "🟢 Secure", "0%", "🔴 High")
            self.data_table.add_row("203.0.113.1", "🔵 Unknown", "25%", "🟡 Medium")

        # Initialize log
        if self.demo_log:
            self.demo_log.write_line("🚀 System initialized")
            self.demo_log.write_line("🔒 Security protocols loaded")
            self.demo_log.write_line("🌐 Network interface active")
            self.demo_log.write_line("⚡ Ready for operations")

    @on(Button.Pressed, "#next-rich-btn")
    def next_rich_demo(self) -> None:
        """Show next Rich demo."""
        if self.rich_showcase:
            self.rich_showcase.next_demo()

    @on(Button.Pressed, "#start-hack")
    async def start_hacking(self) -> None:
        """Start hacking sequence."""
        if self.demo_log:
            self.demo_log.write_line("🚀 [bold red]INITIATING HACK SEQUENCE[/bold red]")
            self.demo_log.write_line("🔍 Scanning for vulnerabilities...")
            await asyncio.sleep(1)
            self.demo_log.write_line("🎯 Target acquired: 192.168.1.100")
            await asyncio.sleep(1)
            self.demo_log.write_line("💥 Exploiting buffer overflow...")
            await asyncio.sleep(2)
            self.demo_log.write_line("✅ [bold green]ACCESS GRANTED![/bold green]")

        # Update progress bars
        system_health = self.query_one("#system-health", ProgressBar)
        system_health.update(progress=85)

    @on(Button.Pressed, "#stealth-mode")
    async def enable_stealth(self) -> None:
        """Enable stealth mode."""
        if self.demo_log:
            self.demo_log.write_line(
                "🛡️ [bold yellow]ACTIVATING STEALTH MODE[/bold yellow]"
            )
            self.demo_log.write_line("🔇 Disabling network signatures...")
            await asyncio.sleep(1)
            self.demo_log.write_line("👻 Spoofing MAC addresses...")
            await asyncio.sleep(1)
            self.demo_log.write_line("🌫️ Enabling traffic obfuscation...")
            await asyncio.sleep(1)
            self.demo_log.write_line("✅ [bold green]STEALTH MODE ACTIVE[/bold green]")

        stealth_level = self.query_one("#stealth-level", ProgressBar)
        stealth_level.update(progress=100)

    @on(Button.Pressed, "#launch-attack")
    async def launch_attack(self) -> None:
        """Launch cyber attack."""
        if self.demo_log:
            self.demo_log.write_line("💥 [bold red]LAUNCHING CYBER ATTACK[/bold red]")
            self.demo_log.write_line("🔥 Deploying payload...")

            attack_progress = self.query_one("#attack-progress", ProgressBar)
            for i in range(0, 101, 10):
                attack_progress.update(progress=i)
                self.demo_log.write_line(f"📊 Attack progress: {i}%")
                await asyncio.sleep(0.5)

            self.demo_log.write_line("🎯 [bold green]ATTACK SUCCESSFUL![/bold green]")
            self.demo_log.write_line("🏆 Target systems compromised")

    @on(Button.Pressed, "#reset-system")
    def reset_system(self) -> None:
        """Reset all systems."""
        if self.demo_log:
            self.demo_log.clear()
            self.demo_log.write_line("🔄 [bold cyan]SYSTEM RESET[/bold cyan]")
            self.demo_log.write_line("🧹 Clearing all traces...")
            self.demo_log.write_line("🔒 Restoring security protocols...")
            self.demo_log.write_line("✅ System restored to default state")

        # Reset progress bars
        for bar_id in ["#system-health", "#stealth-level", "#attack-progress"]:
            bar = self.query_one(bar_id, ProgressBar)
            bar.update(progress=0)

    @on(Button.Pressed, "#generate-data")
    def generate_data(self) -> None:
        """Generate random data."""
        if self.demo_log and self.data_table:
            targets = ["10.0.0.1", "172.16.0.5", "203.0.113.10", "198.51.100.1"]
            statuses = ["🔴 Compromised", "🟡 Scanning", "🟢 Secure", "🔵 Unknown"]
            risks = ["🟢 Low", "🟡 Medium", "🔴 High"]

            target = random.choice(targets)
            status = random.choice(statuses)
            progress = f"{random.randint(0, 100)}%"
            risk = random.choice(risks)

            self.data_table.add_row(target, status, progress, risk)
            self.demo_log.write_line(f"📊 Added new target: {target}")

    @on(Button.Pressed, "#random-action")
    async def random_action(self) -> None:
        """Perform random hacker action."""
        if self.demo_log:
            actions = [
                "🔍 Port scanning initiated...",
                "🛡️ Firewall bypass detected...",
                "🔐 Encryption key cracked...",
                "📡 Network traffic intercepted...",
                "💻 Remote shell established...",
                "🗂️ Database dump completed...",
                "🎭 Identity spoofed successfully...",
                "🌐 Proxy chain established...",
            ]

            action = random.choice(actions)
            self.demo_log.write_line(action)
            await asyncio.sleep(random.uniform(0.5, 2.0))
            self.demo_log.write_line("✅ Operation completed successfully")

    @on(Input.Submitted)
    def handle_input(self, event: Input.Submitted) -> None:
        """Handle input submissions."""
        if self.demo_log and event.value:
            self.demo_log.write_line(f"💬 User input: {event.value}")
            event.input.value = ""

    @on(Checkbox.Changed)
    def handle_checkbox(self, event: Checkbox.Changed) -> None:
        """Handle checkbox changes."""
        if self.demo_log:
            status = "enabled" if event.value else "disabled"
            self.demo_log.write_line(f"🎛️ Hacker mode {status}")

    @on(Switch.Changed)
    def handle_switch(self, event: Switch.Changed) -> None:
        """Handle switch changes."""
        if self.demo_log:
            status = "ON" if event.value else "OFF"
            self.demo_log.write_line(f"🔘 Switch toggled {status}")


def main() -> None:
    """Launch the ultimate Textual and Rich demo."""
    app = UltimateDemo()
    app.run()


if __name__ == "__main__":
    main()
