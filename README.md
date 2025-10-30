# EloTracker

A simple command-line application for tracking your Pokémon GO Battle League Elo progression across daily sets.

## Features

- Record the Elo rating you have after each set (up to 25 sets per day).
- Summarize recent days with the number of sets played, starting/ending Elo, daily change, and highs/lows.
- View your complete history or trim it to the most recent days.
- Reset your tracked data when you want to start fresh.

All data is stored in a JSON file located at `~/.elo_tracker/elo_history.json` by default. You can override the storage directory by setting the `ELO_TRACKER_DATA_DIR` environment variable.

## Getting started

No external dependencies are required. Run the tool directly with Python 3.11+:

```bash
python -m elo_tracker --help
```

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
