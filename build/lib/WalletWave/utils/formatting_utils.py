from datetime import datetime

def format_timestamp(timestamp: int, date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Convert a Unix timestamp to a formatted date string."""
    try:
        return datetime.fromtimestamp(timestamp).strftime(date_format)
    except Exception as e:
        return f"Invalid timestamp: {timestamp} ({e})"

def format_percentage(value: float) -> str:
    """Format a float as a percentage."""
    try:
        return f"{value * 100:.2f}%"
    except Exception as e:
        return f"Invalid percentage: {value} ({e})"

def format_currency(value: float, currency_symbol: str = "$") -> str:
    """Format a float as a currency."""
    try:
        return f"{currency_symbol}{value:,.2f}"
    except Exception as e:
        return f"Invalid currency value: {value} ({e})"

def format_gmgn_time_period(seconds: float) -> str:
    """
    Converts seconds into a more human-readable format of days, hours, minutes, and seconds.

    Args:
        seconds (float): Time period in seconds.

    Returns:
        str: A formatted string showing the time period in days, hours, minutes, and seconds.
    """

    original_seconds = seconds
    try:
        seconds = int(seconds)
        days = seconds // (24 * 3600)
        seconds %= (24 * 3600)
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    except Exception as e:
        return f"Seconds: {str(original_seconds)}: {e}"
