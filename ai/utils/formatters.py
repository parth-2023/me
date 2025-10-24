"""Output formatting utilities for non-API features."""


def print_header(text: str) -> None:
    """Print a formatted header."""
    print("=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_section(text: str) -> None:
    """Print a section header."""
    print(f"\n{'-' * 80}")
    print(f"  {text}")
    print('-' * 80)


def print_result(text: str) -> None:
    """Print a result line."""
    print(f"  {text}")


def format_percentage(value: float) -> str:
    """Format a percentage value."""
    return f"{value:.2f}%"


def format_table_row(columns: list, widths: list) -> str:
    """Format a table row with specified column widths."""
    return " | ".join(str(col).ljust(width) for col, width in zip(columns, widths))


def print_box(title: str, lines: list) -> None:
    """Print content in a box."""
    max_width = max(len(line) for line in [title] + lines)
    border = "=" * (max_width + 4)
    
    print(f"+{border}+")
    print(f"|  {title.ljust(max_width)}  |")
    print(f"+{border}+")
    for line in lines:
        print(f"|  {line.ljust(max_width)}  |")
    print(f"+{border}+")


__all__ = [
    "print_header",
    "print_section",
    "print_result",
    "format_percentage",
    "format_table_row",
    "print_box",
]
