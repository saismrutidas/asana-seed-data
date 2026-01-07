import uuid
import random

from loguru import logger

from utils.db import execute_many
from utils.random import seed_everything, probability


TAG_POOL = [
    "bug",
    "feature",
    "urgent",
    "low-priority",
    "tech-debt",
    "customer-request",
    "blocked",
    "quick-win",
    "needs-review",
    "backend",
    "frontend",
]


def generate_tags(conn, task_ids: list, config: dict = None):
    """
    Generate tags and assign them to tasks.

    Args:
        conn: SQLite connection
        task_ids (list): Task IDs
        config (dict, optional): Configuration values
    """

    if config and "random_seed" in config:
        seed_everything(config["random_seed"])

    # Create tags
    tag_rows = []
    tag_ids = {}

    for tag in TAG_POOL:
        tag_id = str(uuid.uuid4())
        tag_ids[tag] = tag_id
        tag_rows.append((tag_id, tag))

    tag_query = """
        INSERT INTO tags (tag_id, name)
        VALUES (?, ?)
    """

    execute_many(conn, tag_query, tag_rows)

    # Assign tags to tasks
    mapping_rows = []

    for task_id in task_ids:
        if not probability(0.7):
            continue

        num_tags = random.randint(1, 3)
        chosen_tags = random.sample(TAG_POOL, num_tags)

        for tag in chosen_tags:
            mapping_rows.append(
                (
                    task_id,
                    tag_ids[tag]
                )
            )

    mapping_query = """
        INSERT INTO task_tags (task_id, tag_id)
        VALUES (?, ?)
    """

    execute_many(conn, mapping_query, mapping_rows)

    logger.info(
        f"Generated {len(tag_rows)} tags and "
        f"{len(mapping_rows)} task-tag associations"
    )
