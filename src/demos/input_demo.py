#!/usr/bin/env python3
"""
Comprehensive User Input Demo - Rich & Textual
Demonstrates all available user input methods from both libraries.
"""

from datetime import datetime
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, FloatPrompt, IntPrompt, Prompt
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer, Vertical
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Log,
    OptionList,
    RadioButton,
    RadioSet,
    Select,
    Static,
    Switch,
    TabbedContent,
    TabPane,
    TextArea,
)
from textual.widgets.option_list import Option


def rich_prompts_demo() -> None:
    """Demonstrate all Rich prompt types."""
    console = Console()

    console.print(Panel.fit(
        "[bold cyan]🎯 Rich Prompts Demo[/bold cyan]\n"
        "Demonstrating all Rich prompt capabilities",
        style="bright_blue"
    ))

    # Basic text prompt
    console.print("\n[bold yellow]1. Basic Text Prompt[/bold yellow]")
    name = Prompt.ask("Enter your name", default="Anonymous")
    console.print(f"Hello, {name}!")

    # Prompt with choices
    console.print("\n[bold yellow]2. Choice Prompt[/bold yellow]")
    color = Prompt.ask(
        "Choose your favorite color",
        choices=["red", "green", "blue", "yellow"],
        default="blue"
    )
    console.print(f"You chose: [bold {color}]{color}[/bold {color}]")

    # Integer prompt
    console.print("\n[bold yellow]3. Integer Prompt[/bold yellow]")
    age = IntPrompt.ask("Enter your age", default=25)
    console.print(f"You are {age} years old")

    # Float prompt
    console.print("\n[bold yellow]4. Float Prompt[/bold yellow]")
    height = FloatPrompt.ask("Enter your height in meters", default=1.75)
    console.print(f"Your height is {height}m")

    # Confirmation prompt
    console.print("\n[bold yellow]5. Confirmation Prompt[/bold yellow]")
    proceed = Confirm.ask("Do you want to continue?", default=True)
    console.print(f"Continue: {'Yes' if proceed else 'No'}")

    # Password-like prompt (hidden input)
    console.print("\n[bold yellow]6. Hidden Input Prompt[/bold yellow]")
    secret = Prompt.ask("Enter a secret", password=True)
    console.print(f"Secret length: {len(secret)} characters")

    # Prompt with manual validation
    console.print("\n[bold yellow]7. Validated Prompt (Manual)[/bold yellow]")

    def validate_email(email: str) -> str:
        if "@" not in email:
            raise ValueError("Please enter a valid email address")
        return email

    try:
        email = Prompt.ask("Enter your email")
        validate_email(email)  # Manual validation
        console.print(f"Email: {email}")
    except (KeyboardInterrupt, ValueError) as e:
        if isinstance(e, ValueError):
            console.print(f"[red]Validation error: {e}[/red]")
        else:
            console.print("[red]Skipped email validation[/red]")

    # Custom validation with manual checking
    console.print("\n[bold yellow]8. Custom Validation (Manual)[/bold yellow]")

    def validate_username(username: str) -> str:
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not username.isalnum():
            raise ValueError("Username must be alphanumeric")
        return username

    try:
        username = Prompt.ask("Enter username (3+ alphanumeric chars)")
        validate_username(username)  # Manual validation
        console.print(f"Username: {username}")
    except (KeyboardInterrupt, ValueError) as e:
        if isinstance(e, ValueError):
            console.print(f"[red]Validation error: {e}[/red]")
        else:
            console.print("[red]Skipped username validation[/red]")

    console.print("\n[bold green]✅ Rich prompts demo completed![/bold green]")


class TextualInputDemo(App):
    """Comprehensive Textual input widgets demonstration."""

    CSS = """
    Screen {
        background: #001122;
    }

    .header {
        height: 3;
        background: #003366;
        color: #00ff00;
        border: solid #00ff00;
    }

    .demo-container {
        height: 1fr;
        background: #001122;
        padding: 1;
    }

    .input-section {
        background: #002244;
        border: solid #00ffff;
        margin: 1;
        padding: 1;
    }

    .log-section {
        background: #002244;
        border: solid #ffff00;
        margin: 1;
        padding: 1;
        height: 1fr;
    }

    Input {
        background: #003366;
        color: #00ffff;
        border: solid #00ffff;
        margin: 1 0;
    }

    TextArea {
        background: #003366;
        color: #00ffff;
        border: solid #00ffff;
        margin: 1 0;
        height: 6;
    }

    Select {
        background: #003366;
        color: #ffff00;
        border: solid #ffff00;
        margin: 1 0;
    }

    Button {
        background: #003366;
        color: #00ff00;
        border: solid #00ff00;
        margin: 1;
    }

    Button:hover {
        background: #004488;
        color: #ffffff;
    }

    Checkbox {
        background: #003366;
        color: #00ff00;
        margin: 1 0;
    }

    Switch {
        background: #003366;
        margin: 1 0;
    }

    RadioButton {
        background: #003366;
        color: #00ff00;
        margin: 1 0;
    }

    Log {
        background: #003366;
        color: #00ff00;
        border: solid #00ff00;
    }

    ListView {
        background: #003366;
        color: #00ffff;
        border: solid #00ffff;
        margin: 1 0;
        height: 8;
    }

    OptionList {
        background: #003366;
        color: #ffff00;
        border: solid #ffff00;
        margin: 1 0;
        height: 8;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.log: Log | None = None
        self.form_data: dict[str, Any] = {}

    def compose(self) -> ComposeResult:
        """Create the application layout."""
        yield Header()

        with TabbedContent():
            # Basic Input Widgets Tab
            with TabPane("Basic Inputs", id="basic-inputs"):
                with ScrollableContainer():
                    yield Static("[bold cyan]📝 Basic Input Widgets[/bold cyan]")

                    with Container(classes="input-section"):
                        yield Static("[bold yellow]Text Input[/bold yellow]")
                        yield Input(
                            placeholder="Enter your name...",
                            id="name-input"
                        )

                        yield Static("[bold yellow]Password Input[/bold yellow]")
                        yield Input(
                            placeholder="Enter password...",
                            password=True,
                            id="password-input"
                        )

                        yield Static("[bold yellow]Number Input[/bold yellow]")
                        yield Input(
                            placeholder="Enter a number...",
                            type="number",
                            id="number-input"
                        )

                        yield Static("[bold yellow]Multi-line Text Area[/bold yellow]")
                        yield TextArea(
                            "Type your message here...\nSupports multiple lines!",
                            id="message-textarea"
                        )

            # Selection Widgets Tab
            with TabPane("Selection", id="selection-widgets"):
                with ScrollableContainer():
                    yield Static("[bold cyan]🎯 Selection Widgets[/bold cyan]")

                    with Container(classes="input-section"):
                        yield Static("[bold yellow]Dropdown Select[/bold yellow]")
                        yield Select(
                            [
                                ("Python", "python"),
                                ("JavaScript", "javascript"),
                                ("Rust", "rust"),
                                ("Go", "go"),
                                ("TypeScript", "typescript"),
                            ],
                            prompt="Choose your favorite language",
                            id="language-select"
                        )

                        yield Static("[bold yellow]Radio Button Group[/bold yellow]")
                        with RadioSet(id="theme-radio"):
                            yield RadioButton("🌙 Dark Theme", id="dark-theme")
                            yield RadioButton("☀️ Light Theme", id="light-theme")
                            yield RadioButton("🌈 Auto Theme", id="auto-theme")

                        yield Static("[bold yellow]Checkboxes[/bold yellow]")
                        yield Checkbox("📧 Email notifications", id="email-checkbox")
                        yield Checkbox("📱 SMS notifications", id="sms-checkbox")
                        yield Checkbox("🔔 Push notifications", id="push-checkbox")

                        yield Static("[bold yellow]Toggle Switch[/bold yellow]")
                        yield Switch(value=True, id="feature-switch")
                        yield Label("Enable advanced features")

            # Advanced Widgets Tab
            with TabPane("Advanced", id="advanced-widgets"):
                with ScrollableContainer():
                    yield Static("[bold cyan]🚀 Advanced Input Widgets[/bold cyan]")

                    with Container(classes="input-section"):
                        yield Static("[bold yellow]Option List[/bold yellow]")
                        yield OptionList(
                            Option("🔥 Hack the mainframe", id="hack"),
                            Option("🛡️ Enable security protocols", id="security"),
                            Option("🚀 Launch cyber attack", id="attack"),
                            Option("💻 Access database", id="database"),
                            Option("🌐 Connect to network", id="network"),
                            id="action-options"
                        )

                        yield Static("[bold yellow]List View[/bold yellow]")
                        yield ListView(
                            ListItem(Label("📁 Documents")),
                            ListItem(Label("🖼️ Images")),
                            ListItem(Label("🎵 Music")),
                            ListItem(Label("🎬 Videos")),
                            ListItem(Label("📦 Downloads")),
                            id="folder-list"
                        )

            # Form Demo Tab
            with TabPane("Form Demo", id="form-demo"):
                with Horizontal():
                    with Vertical(classes="input-section"):
                        yield Static("[bold cyan]📋 Complete Form Example[/bold cyan]")

                        yield Static("[bold yellow]Personal Information[/bold yellow]")
                        yield Input(placeholder="First Name", id="first-name")
                        yield Input(placeholder="Last Name", id="last-name")
                        yield Input(placeholder="Email", id="email")
                        yield Input(placeholder="Age", type="number", id="age")

                        yield Static("[bold yellow]Preferences[/bold yellow]")
                        yield Select(
                            [
                                ("Beginner", "beginner"),
                                ("Intermediate", "intermediate"),
                                ("Advanced", "advanced")
                            ],
                            prompt="Skill Level",
                            id="skill-level"
                        )

                        with RadioSet(id="contact-method"):
                            yield RadioButton("📧 Email", id="contact-email")
                            yield RadioButton("📱 Phone", id="contact-phone")
                            yield RadioButton("💬 Chat", id="contact-chat")

                        yield Checkbox("📰 Subscribe to newsletter", id="newsletter")
                        yield Checkbox("🔒 Enable two-factor auth", id="2fa")

                        yield TextArea("Additional comments...", id="comments")

                        yield Button(
                            "📤 Submit Form", id="submit-form", variant="success"
                        )
                        yield Button(
                            "🔄 Reset Form", id="reset-form", variant="warning"
                        )

                    with Container(classes="log-section"):
                        yield Static("[bold green]📊 Event Log[/bold green]")
                        self.log = Log(id="event-log")
                        yield self.log

        yield Footer()

    def on_mount(self) -> None:
        """Initialize the application."""
        if self.log:
            self.log.write_line("🚀 Textual Input Demo started!")
            self.log.write_line("💡 Try interacting with the widgets above")

    # Event handlers for all input widgets
    @on(Input.Submitted)
    def handle_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submissions."""
        if self.log:
            self.log.write_line(f"📝 Input '{event.input.id}': {event.value}")
            self.form_data[event.input.id or "unknown"] = event.value

    @on(Input.Changed)
    def handle_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        if self.log and event.value:
            preview = event.value[:20] + "..." if len(event.value) > 20 else event.value
            self.log.write_line(f"✏️ Typing in '{event.input.id}': {preview}")

    @on(TextArea.Changed)
    def handle_textarea_changed(self, event: TextArea.Changed) -> None:
        """Handle textarea changes."""
        if self.log:
            lines = len(event.text_area.text.split('\n'))
            chars = len(event.text_area.text)
            self.log.write_line(
                f"📄 TextArea '{event.text_area.id}': {lines} lines, {chars} chars"
            )

    @on(Select.Changed)
    def handle_select_changed(self, event: Select.Changed) -> None:
        """Handle select changes."""
        if self.log:
            self.log.write_line(f"🎯 Select '{event.select.id}': {event.value}")
            self.form_data[event.select.id or "unknown"] = event.value

    @on(RadioSet.Changed)
    def handle_radio_changed(self, event: RadioSet.Changed) -> None:
        """Handle radio button changes."""
        if self.log:
            self.log.write_line(f"📻 Radio '{event.radio_set.id}': {event.pressed.id}")
            self.form_data[event.radio_set.id or "unknown"] = event.pressed.id

    @on(Checkbox.Changed)
    def handle_checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Handle checkbox changes."""
        if self.log:
            status = "✅ checked" if event.value else "❌ unchecked"
            self.log.write_line(f"☑️ Checkbox '{event.checkbox.id}': {status}")
            self.form_data[event.checkbox.id or "unknown"] = event.value

    @on(Switch.Changed)
    def handle_switch_changed(self, event: Switch.Changed) -> None:
        """Handle switch changes."""
        if self.log:
            status = "🟢 ON" if event.value else "🔴 OFF"
            self.log.write_line(f"🔘 Switch '{event.switch.id}': {status}")
            self.form_data[event.switch.id or "unknown"] = event.value

    @on(OptionList.OptionSelected)
    def handle_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle option list selections."""
        if self.log:
            self.log.write_line(f"📋 Option selected: {event.option.prompt}")
            self.form_data["selected_option"] = str(event.option.id)

    @on(ListView.Selected)
    def handle_list_selected(self, event: ListView.Selected) -> None:
        """Handle list view selections."""
        if self.log:
            self.log.write_line(f"📁 List item selected: {event.item.id}")
            self.form_data["selected_folder"] = str(event.item.id)

    @on(Button.Pressed, "#submit-form")
    def handle_submit_form(self) -> None:
        """Handle form submission."""
        if self.log:
            self.log.write_line("📤 [bold green]FORM SUBMITTED![/bold green]")
            self.log.write_line("📊 Form data:")
            for key, value in self.form_data.items():
                self.log.write_line(f"   • {key}: {value}")

            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"form_data_{timestamp}.txt"
            try:
                with open(filename, "w") as f:
                    f.write(f"Form Data - {datetime.now()}\n")
                    f.write("=" * 40 + "\n")
                    for key, value in self.form_data.items():
                        f.write(f"{key}: {value}\n")
                self.log.write_line(f"💾 Data saved to {filename}")
            except Exception as e:
                self.log.write_line(f"❌ Error saving: {e}")

    @on(Button.Pressed, "#reset-form")
    def handle_reset_form(self) -> None:
        """Handle form reset."""
        if self.log:
            self.log.write_line("🔄 [bold yellow]FORM RESET![/bold yellow]")
            self.form_data.clear()

            # Reset all form fields
            for widget in self.query("Input"):
                widget.value = ""

            for widget in self.query("TextArea"):
                widget.text = ""

            for widget in self.query("Select"):
                widget.value = Select.BLANK

            for widget in self.query("Checkbox"):
                widget.value = False

            for widget in self.query("Switch"):
                widget.value = False


def main() -> None:
    """Main function to run both demos."""
    console = Console()

    console.print(Panel.fit(
        "[bold magenta]🎮 Complete User Input Demo[/bold magenta]\n"
        "Rich Prompts + Textual Widgets",
        style="bright_magenta"
    ))

    # Ask which demo to run
    demo_choice = Prompt.ask(
        "Which demo would you like to run?",
        choices=["rich", "textual", "both"],
        default="both"
    )

    if demo_choice in ["rich", "both"]:
        rich_prompts_demo()

        if demo_choice == "both":
            console.print("\n" + "="*50)
            proceed = Confirm.ask("Continue to Textual demo?", default=True)
            if not proceed:
                return

    if demo_choice in ["textual", "both"]:
        console.print(Panel.fit(
            "[bold cyan]🚀 Starting Textual Interactive Demo[/bold cyan]\n"
            "Use Tab/Shift+Tab to navigate, Enter to interact",
            style="bright_cyan"
        ))

        app = TextualInputDemo()
        app.run()


if __name__ == "__main__":
    main()
