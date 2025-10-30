"""Command line interface for the EloTracker application."""

from __future__ import annotations

import argparse
from datetime import date, timedelta
from typing import Iterable, List

from .storage import EloData, EloDay, load_data, save_data


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        msg = "Dates must be supplied in ISO format (YYYY-MM-DD)."
        raise argparse.ArgumentTypeError(msg) from exc


def format_change(change: int | None) -> str:
    if change is None:
        return "-"
    sign = "+" if change >= 0 else ""
    return f"{sign}{change}"


def format_optional(value: int | None) -> str:
    return str(value) if value is not None else "-"


def summarize_day(day: EloDay) -> List[str]:
    return [
        day.date.isoformat(),
        str(len(day.sets)),
        format_optional(day.start),
        format_optional(day.end),
        format_change(day.change),
        format_optional(day.best),
        format_optional(day.worst),
    ]


def render_table(headers: Iterable[str], rows: Iterable[Iterable[str]]) -> str:
    col_widths = [len(header) for header in headers]
    row_list = []
    for row in rows:
        row_values = list(row)
        for idx, value in enumerate(row_values):
            col_widths[idx] = max(col_widths[idx], len(value))
        row_list.append(row_values)

    def format_row(row_values: Iterable[str]) -> str:
        parts = [value.ljust(col_widths[idx]) for idx, value in enumerate(row_values)]
        return " | ".join(parts)

    header_line = format_row(headers)
    separator = "-+-".join("-" * width for width in col_widths)
    body_lines = [format_row(row) for row in row_list]
    return "\n".join([header_line, separator, *body_lines]) if body_lines else header_line


def cmd_record(args: argparse.Namespace) -> None:
    data = load_data()
    record_date = args.date or date.today()
    day = data.get_day(record_date)
    day.sets.append(args.elo)
    save_data(data)
    print(
        f"Recorded set #{len(day.sets)} for {record_date.isoformat()} with Elo {args.elo}."
    )


def cmd_summary(args: argparse.Namespace) -> None:
    data = load_data()
    days = data.sorted_days()
    if args.date:
        target = args.date.isoformat()
        days = [day for day in days if day.date.isoformat() == target]
    elif args.days is not None:
        cutoff = date.today() - timedelta(days=args.days - 1)
        days = [day for day in days if day.date >= cutoff]

    if not days:
        print("No Elo data recorded yet. Use the 'record' command to add a set.")
        return

    headers = ["Date", "Sets", "Start", "End", "Δ Elo", "Peak", "Low"]
    rows = [summarize_day(day) for day in days]
    print(render_table(headers, rows))


def cmd_history(args: argparse.Namespace) -> None:
    data = load_data()
    days = data.sorted_days()
    if not days:
        print("No Elo data recorded yet. Use the 'record' command to add a set.")
        return

    headers = ["Date", "Sets", "Start", "End", "Δ Elo", "Peak", "Low"]
    if args.limit is not None:
        days = days[-args.limit :]
    rows = [summarize_day(day) for day in days]
    print(render_table(headers, rows))


def cmd_reset(args: argparse.Namespace) -> None:
    confirmation = input(
        "This will delete all tracked Elo data. Type 'yes' to confirm: "
    ).strip()
    if confirmation.lower() != "yes":
        print("Reset cancelled.")
        return

    data = EloData()
    save_data(data)
    print("All Elo data has been cleared.")


COMMANDS = {
    "record": cmd_record,
    "summary": cmd_summary,
    "history": cmd_history,
    "reset": cmd_reset,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Track Pokémon GO GBL Elo progression for each daily set."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    record_parser = subparsers.add_parser("record", help="Record the Elo after a set")
    record_parser.add_argument("elo", type=int, help="Elo rating after the set")
    record_parser.add_argument(
        "--date",
        type=parse_date,
        help="Day to record the set for (defaults to today)",
    )
    record_parser.set_defaults(func=cmd_record)

    summary_parser = subparsers.add_parser(
        "summary", help="Show a summary for a date or recent days"
    )
    summary_parser.add_argument(
        "--date", type=parse_date, help="Specific date to summarize (YYYY-MM-DD)"
    )
    summary_parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of recent days to include in the summary",
    )
    summary_parser.set_defaults(func=cmd_summary)

    history_parser = subparsers.add_parser(
        "history", help="Show all recorded Elo history"
    )
    history_parser.add_argument(
        "--limit",
        type=int,
        help="Only display the most recent N days",
    )
    history_parser.set_defaults(func=cmd_history)

    reset_parser = subparsers.add_parser("reset", help="Delete all Elo history")
    reset_parser.set_defaults(func=cmd_reset)

    return parser


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "func", None)
    if handler is None:
        parser.print_help()
        return
    handler(args)


if __name__ == "__main__":
    main()
