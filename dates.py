import random
from datetime import datetime, timedelta


def random_past_datetime(days_back: int) -> datetime:
    """
    Generate a random datetime within the past N days.
    """
    now = datetime.utcnow()
    delta_days = random.randint(0, days_back)
    delta_seconds = random.randint(0, 86400)
    return now - timedelta(days=delta_days, seconds=delta_seconds)


def random_future_date(max_days: int = 90):
    """
    Generate a random future date (or None).
    """
    return (datetime.utcnow() + timedelta(days=random.randint(1, max_days))).date()


def maybe_due_date():
    """
    Realistic due-date distribution:
    - 10% no due date
    - 90% has due date within 1–90 days
    """
    if random.random() < 0.1:
        return None
    return random_future_date()


def completion_time(created_at: datetime):
    """
    Generate a realistic completion timestamp after creation.
    """
    delta_days = random.randint(1, 14)
    return created_at + timedelta(days=delta_days)
