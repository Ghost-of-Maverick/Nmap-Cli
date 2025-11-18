# 🛰️ Nmap Shell - Command Line Interface for Nmap

<p align="center">
  <img src="logo/logo.png" width="200" alt="nmapShell logo">
</p>

**Nmap Shell** is an interactive and user-friendly command-line shell built to simplify running **Nmap scans**, managing predefined scan profiles, viewing previous results, and keeping a persistent scan history.  
It features command autocompletion, session history, a colorful interface, and a workflow similar to a mini security scanning terminal.

---

## 🚀 Features

- Interactive CLI shell using `prompt_toolkit`
- Autocompletion for all commands
- Beautiful tables and output formatting with `rich`
- Predefined Nmap scan profiles
- Support for fully custom Nmap arguments
- Local SQLite database storing scan history
- View previous scans by ID
- Console clearing and safe history cleaning
- Modular and extensible codebase

---

## 📦 Requirements

- **Python 3.8 or newer**
- **Nmap installed** on your system (the `nmap` command must be available)
- Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Installation

Clone the repository:

```
git clone https://github.com/Ghost-of-Maverick/Nmap-Shell.git
cd Nmap-Shell/
```

(Optional) Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

Install dependencies:

```
pip install -r requirements.txt
```

Make sure nmap is installed and in PATH.

Debian/Ubuntu:

```
sudo apt update
sudo apt install nmap
```

macOS (Homebrew):

```
brew install nmap
```

## ▶️ Running the Application

Start the interactive shell:

```
python3 app.py
```

You will then see:

```
nmapShell>
```

From here, you can use all available commands.

## 🧭 How It Works

The CLI loop is built with `PromptSession`, providing:

- Autocompletion
- Highlighted prompt input
- History navigation

The application maintains an internal state with:

- Target
- Scan type

### Scan Execution Flow

1. You set a target and choose a scan profile.
2. `run_scan()` executes Nmap with the chosen arguments.
3. Output is captured and stored in an SQLite database with:
   - Target
   - Scan type
   - Nmap command
   - Full output
   - Timestamp
4. Output is printed using `rich`.

Review past scans:

```
history
view <id>
```

Delete all saved scans:

```
clean
```

## 📝 Available Commands

| Command              | Description                             |
| -------------------- | --------------------------------------- |
| `set target <value>` | Set the target IP or domain             |
| `set scan`           | Select a scan type from a numbered list |
| `show options`       | Display current target and scan type    |
| `run`                | Execute the configured Nmap scan        |
| `history`            | Display all saved scans                 |
| `view <id>`          | View the full output of a saved scan    |
| `clean`              | Delete all scan history                 |
| `clear`              | Clear the console screen                |
| `help`               | Show all commands                       |
| `exit`, `quit`       | Exit the program                        |

## 📚 Scan Profiles (example)

Defined in `scan_profiles.py`:

```
scan_profiles = {
    "Ping Scan": ["-sn"],
    "Quick Scan": ["-T4", "-F"],
    "Port Scan": ["-sS", "-p", "1-1000"],
    "Aggressive Scan": ["-A"],
    "OS Detection": ["-O"],
    "Version Detection": ["-sV"],
    "Custom": []
}
```

Choosing `Custom` will prompt the user for custom Nmap arguments.

## 🧩 Autocompletion (example)

Powered by `NestedCompleter` from `prompt_toolkit`:

```
from prompt_toolkit.completion import NestedCompleter

command_completer = NestedCompleter.from_nested_dict({
    "set": {
        "target": None,
        "scan": None,
    },
    "show": {
        "options": None,
    },
    "run": None,
    "history": None,
    "view": {
        "<id>": None
    },
    "clear": None,
    "help": None,
    "exit": None,
    "quit": None,
})
```

## 🧱 Project Structure

```
nmapShell/
├── logo/                # App logo (logo/logo.png)
├── completer.py         # Autocompletion logic
├── scanner.py           # run_scan() wrapper around nmap
├── scan_profiles.py     # Predefined scan profiles dict
├── db.py                # SQLite database functions
├── utils.py             # Banner and helper utilities
├── state.py             # AppState class (holds target and scan_type)
├── app.py               # Interactive shell (entry point)
└── requirements.txt
```

## 🧹 Clearing Scan History

To delete all saved scan entries:

```
clean
```

This calls `clear_scan_history()` in `db.py`.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file in the project root for full details.

## ⚠️ Legal Disclaimer

This tool is intended only for authorized security testing.
Do not scan systems without explicit permission.
You are responsible for all actions performed with this software.

