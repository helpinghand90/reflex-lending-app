import uuid
import base64
import string
import random


def generate_short_alphanumeric_uuid(prefix: str):
    """
    Generates a short, alphanumeric UUID. with a defined suffix
    
    Returns:
      a string with the format: prefix-<alphanumeric_uuid>
    """
    uuid_bytes = uuid.uuid4().bytes
    encoded_uuid = base64.b64encode(uuid_bytes).decode("ascii")

    # Replace non-alphanumeric characters with random letters
    valid_chars = string.ascii_letters + string.digits
    alphanumeric_uuid = "".join(
        c if c in valid_chars else random.choice(valid_chars) for c in encoded_uuid
    )
    return f"{prefix.upper()}-{alphanumeric_uuid.rstrip('=')}"


def complete_months_between(start_date, end_date):
    """
    Calculates the number of complete months between two dates.

    Args:
      start_date: The start date (datetime.date).
      end_date: The end date (datetime.date).

    Returns:
      The number of complete months between the two dates.
    """
    if start_date > end_date:
        raise ValueError("Start date must be before end date")

    years_diff = end_date.year - start_date.year
    months_diff = end_date.month - start_date.month

    # Adjust for day of the month
    if end_date.day < start_date.day:
        months_diff -= 1

    total_months = years_diff * 12 + months_diff
    return max(total_months, 0)  # Ensure result is not negative
