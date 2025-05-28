
from typing import Optional, List, Dict, Union
def get_user_input(prompt, required=True, valid_options=None):
    """
    Prompt the user for input, optionally enforce required input
    or restrict to valid options.
    """
    while True:
        value = input(prompt).strip()
        if not value and required:
            print("Input is required, please try again.")
            continue
        if valid_options and value not in valid_options:
            print(f"Invalid option. Choose from: {', '.join(valid_options)}")
            continue
        return value


def validate_positive_number(value: str) -> Optional[Union[int, float]]:
    """
    Check if the input value can be converted to a positive number (int or float).
    Return the number if valid, else None.
    """
    try:
        num = float(value)
        if num > 0:
            return num
    except ValueError:
        pass
    return None


def format_table(data: List[Dict[str, Union[str, int, float]]], headers: Optional[List[str]] = None) -> str:
    """
    Format a list of dictionaries or list of tuples into a readable table string.
    """
    if not data:
        return "No data available."
    
    # If data is list of dicts, convert to list of tuples
    if isinstance(data[0], dict):
        if not headers:
            headers = list(data[0].keys())
        rows = [tuple(d[h] for h in headers) for d in data]
    else:
        rows = data
        if not headers:
            headers = [f"Col{i+1}" for i in range(len(rows[0]))]

    # Calculate column widths
    col_widths = [max(len(str(item)) for item in [header] + [row[i] for row in rows]) for i, header in enumerate(headers)]
    
    # Build header line
    header_line = " | ".join(header.ljust(col_widths[i]) for i, header in enumerate(headers))
    separator = "-+-".join("-" * col_width for col_width in col_widths)

    # Build rows
    row_lines = []
    for row in rows:
        row_line = " | ".join(str(item).ljust(col_widths[i]) for i, item in enumerate(row))
        row_lines.append(row_line)
    
    table_str = f"{header_line}\n{separator}\n" + "\n".join(row_lines)
    return table_str


def confirm_action(prompt="Are you sure? (y/n): "):
    """
    Prompt user for yes/no confirmation.
    """
    while True:
        choice = input(prompt).strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'.")


def parse_date(date_str):
    """
    Try to parse a date string to a datetime.date object.
    Return None if invalid.
    """
    from datetime import datetime
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None
