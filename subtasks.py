import uuid
import random

from loguru import logger

from utils.db import execute_many
from utils.dates import random_past_datetime, completion_time
from utils.random import seed_everything, probability


SUBTASK_TEMPLATES = [
    "Investigate issue",
    "Implement fix",
    "Add tests",
    "Update documentation",
    "Perform code review",
    "Verify in staging",
]


def generate_subtasks(
    conn,
    task_ids: list,
    user_ids: list,
    config: dict,
):
    """
    Generate subtasks for a subset of tasks.

    Args:
        conn: SQLite connection
        task_ids (list): Parent task IDs
        user_ids (list): User IDs
        config (dict): Configuration values
    """

    seed_everything(config["random_seed"])

    subtask_ratio = config["subtask_ratio"]
    history_days = config["history_days"]

    rows = []

    for task_id in task_ids:
        # Only some tasks have subtasks
        if not probability(subtask_ratio):
            continue

        num_subtasks = random.randint(1, 4)

        for _ in range(num_subtasks):
            subtask_id = str(uuid.uuid4())
            name = random.choice(SUBTASK_TEMPLATES)

            created_at = random_past_datetime(history_days)
            completed = probability(0.6)
            completed_at = (
                completion_time(created_at).isoformat()
                if completed
                else None
            )

            assignee_id = (
                random.choice(user_ids)
                if probability(0.75)
                else None
            )

            rows.append(
                (
                    subtask_id,
                    task_id,
                    assignee_id,
                    name,
                    completed,
                    created_at.isoformat(),
                    completed_at,
                )
            )

    query = """
        INSERT INTO subtasks (
            subtask_id,
            parent_task_id,
            assignee_id,
            name,
            completed,
            created_at,
            completed_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    execute_many(conn, query, rows)

    logger.info(f"Generated {len(rows)} subtasks")
