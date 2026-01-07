import uuid
import random
from datetime import datetime

from faker import Faker
from loguru import logger

from utils.db import execute_many
from utils.dates import random_past_datetime
from utils.random import seed_everything

fake = Faker()


def generate_users(conn, org_id: str, config: dict):
    """
    Generate users for the organization.

    Args:
        conn: SQLite connection
        org_id (str): Organization ID
        config (dict): Configuration values

    Returns:
        List[str]: Generated user IDs
    """

    seed_everything(config["random_seed"])

    num_users = config["num_users"]
    history_days = config["history_days"]

    rows = []
    user_ids = []

    for i in range(num_users):
        user_id = str(uuid.uuid4())
        full_name = fake.name()

        email = (
            full_name.lower()
            .replace(" ", ".")
            .replace("'", "")
            + f".{i}"
            + "@acmecloud.com"
        )


        # Small percentage of admins
        role = "admin" if random.random() < 0.05 else "member"

        joined_at = random_past_datetime(history_days).isoformat()

        rows.append(
            (
                user_id,
                org_id,
                full_name,
                email,
                role,
                joined_at
            )
        )
        user_ids.append(user_id)

    query = """
        INSERT INTO users (
            user_id, org_id, full_name, email, role, joined_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """

    execute_many(conn, query, rows)

    logger.info(f"Generated {len(user_ids)} users")

    return user_ids
