# EloTracker

A simple command-line application for tracking your Pokémon GO Battle League Elo progression across daily sets.

## Features

- Record the Elo rating you have after each set (up to 25 sets per day).
- Summarize recent days with the number of sets played, starting/ending Elo, daily change, and highs/lows.
- View your complete history or trim it to the most recent days.
- Reset your tracked data when you want to start fresh.

All data is stored in a JSON file located at `~/.elo_tracker/elo_history.json` by default. You can override the storage directory by setting the `ELO_TRACKER_DATA_DIR` environment variable.

## Getting started

### 1. Install Python 3.11+

The tracker is a plain Python module, so make sure a recent Python interpreter is available. You can check your version with:

```bash
python --version
```

If your system uses `python3` for modern interpreters, just substitute `python3` in every command below.

### 2. Clone the repository (optional)

If you have not already downloaded the project, clone it and change into the new directory:

```bash
git clone https://github.com/your-account/elo-tracker.git
cd elo-tracker
```

### 3. (Optional) Create a virtual environment

Virtual environments keep project dependencies isolated. The tracker has no external dependencies, but you can still create one if you prefer:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

### 4. Install the package (recommended)

Installing the tracker ensures the `elo_tracker` module is available no matter which directory you are in. From the project root run:

```bash
python -m pip install --editable .
```

The editable flag (`-e`) keeps the installation linked to your working copy, so any local changes are reflected immediately when you run the command-line tool.

### 5. Run the command-line app

The tracker is run with Python’s module flag:

```bash
python -m elo_tracker --help
```

You should see the built-in help output describing each command. Once the package has been installed you can run the same command from any directory or use the convenience script:

```bash
elo-tracker --help
```

The examples below assume you are running the command from the project root.

### Record a set

```bash
python -m elo_tracker record 2150
```

The command above records an Elo of 2150 for today. Include `--date YYYY-MM-DD` to log a past day.

### Show recent summaries

```bash
python -m elo_tracker summary --days 5
```

This prints a table summarizing the last five days of recorded sets. Provide `--date YYYY-MM-DD` to focus on a specific day.

### View history

```bash
python -m elo_tracker history
```

Add `--limit N` to only view the most recent `N` days.

### Reset data

```bash
python -m elo_tracker reset
```

You will be asked to confirm before all recorded data is deleted.
