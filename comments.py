import uuid
import random

from loguru import logger

from utils.db import execute_many
from utils.dates import random_past_datetime
from utils.random import seed_everything, probability


COMMENT_TEMPLATES = [
    "Started working on this.",
    "Blocked due to dependency, will update.",
    "PR is up for review.",
    "This should be ready by EOD.",
    "Can someone please take a look?",
    "Following up on this.",
    "I think this is resolved now.",
    "Waiting for confirmation from stakeholders.",
    "Added more details to the description.",
    "Marking this as done.",
]


def generate_comments(
    conn,
    task_ids: list,
    user_ids: list,
    config: dict = None,
):
    """
    Generate comments for a subset of tasks.

    Args:
        conn: SQLite connection
        task_ids (list): Task IDs
        user_ids (list): User IDs
        config (dict, optional): Configuration values
    """

    if config and "random_seed" in config:
        seed_everything(config["random_seed"])

    rows = []

    for task_id in task_ids:
        # Only some tasks receive comments
        if not probability(0.6):
            continue

        num_comments = random.randint(1, 5)

        commenters = random.sample(
            user_ids,
            k=min(len(user_ids), random.randint(1, 3))
        )

        for _ in range(num_comments):
            comment_id = str(uuid.uuid4())
            user_id = random.choice(commenters)
            body = random.choice(COMMENT_TEMPLATES)
            created_at = random_past_datetime(180).isoformat()

            rows.append(
                (
                    comment_id,
                    task_id,
                    user_id,
                    body,
                    created_at,
                )
            )

    query = """
        INSERT INTO comments (
            comment_id,
            task_id,
            user_id,
            body,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
    """

    execute_many(conn, query, rows)

    logger.info(f"Generated {len(rows)} comments")
