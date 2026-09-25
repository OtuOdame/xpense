import argparse


def positive_float(value):
    """Validate that --amount is a positive number."""
    try:
        f = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid number")
    if f <= 0:
        raise argparse.ArgumentTypeError("Amount must be greater than zero")
    return f