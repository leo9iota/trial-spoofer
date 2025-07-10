# 🔒 Linux VS Code Spoofer

A beautiful TUI application built with Rich that resets host fingerprints for VS Code extensions like Augment Code and Cursor.

## ✨ Features

- **🎨 Beautiful Rich TUI** - Stunning terminal interface with progress bars, tables, and panels
- **🛡️ Comprehensive Spoofing** - MAC address, machine ID, filesystem UUID, hostname, and cache cleaning
- **⚡ Modular Architecture** - Clean separation of concerns across utility modules
- **🔧 Configurable** - Interactive and non-interactive modes
- **📊 Real-time Progress** - Live progress tracking with spinners and progress bars

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Root privileges (for system modifications)
- `uv` package manager (recommended)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd vscode-spoofer

# Install dependencies
uv sync

# Run the application
sudo uv run python src/main.py
```

### Demo Mode

To see the beautiful TUI without requiring root privileges:

```bash
uv run python src/demo.py
```

## 🏗️ Project Structure

```
src/
├── main.py              # Main TUI application
├── demo.py              # Demo without root requirements
└── utils/
    ├── helper.py         # Core utilities and argument parsing
    ├── spoofer.py        # MAC, machine ID, and filesystem UUID spoofing
    ├── system.py         # Hostname changes and boot configuration
    └── cleaner.py        # VS Code cache cleaning
```

## 🎯 Available Operations

| Feature | Description | Risk Level |
|---------|-------------|------------|
| **MAC Address** | Spoof network interface MAC | 🟢 Low |
| **Machine ID** | Regenerate system machine-id | 🟢 Low |
| **Filesystem UUID** | Randomize root filesystem UUID | 🟡 Medium |
| **Hostname** | Set random hostname | 🟢 Low |
| **VS Code Caches** | Purge editor caches | 🟢 Low |
| **New User** | Create sandbox user account | 🟢 Low |

## 🔧 Usage

### Interactive Mode (Default)

```bash
sudo uv run python src/main.py
```

### Non-Interactive Mode

```bash
sudo uv run python src/main.py --non-interactive
```

### Skip UUID Changes

```bash
sudo uv run python src/main.py --no-uuid
```

## 🎨 TUI Features

- **Rich Headers** - Beautiful styled application headers
- **Feature Tables** - Clear overview of available security features
- **Interactive Prompts** - User-friendly confirmation dialogs
- **Live Progress** - Real-time progress tracking with spinners
- **Status Panels** - Clear success/failure reporting
- **Color-coded Results** - Green for success, red for failures

## ⚠️ Important Notes

- **Root Required**: Most operations require root privileges
- **Backup Recommended**: Consider backing up important system files
- **Reboot Needed**: Some changes require a system reboot to take full effect
- **Test First**: Use the demo mode to familiarize yourself with the interface

## 🛠️ Development

### Code Style

The project uses:
- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

### Testing

```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src
```

## Tech Stack

![Tech Stack](https://go-skill-icons.vercel.app/api/icons?i=python)

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 🔗 Dependencies

- **Rich** - Beautiful terminal interfaces
- **Textual** - Advanced TUI framework (future use)
