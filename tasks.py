import uuid
import random
from datetime import datetime

from loguru import logger

from utils.db import execute_many
from utils.dates import (
    random_past_datetime,
    maybe_due_date,
    completion_time,
)
from utils.random import seed_everything, probability


ENGINEERING_TASKS = [
    "Implement API endpoint",
    "Refactor service module",
    "Fix production bug",
    "Add unit tests",
    "Improve query performance",
    "Update CI pipeline",
]

MARKETING_TASKS = [
    "Draft campaign copy",
    "Design landing page",
    "Schedule email blast",
    "Prepare social media assets",
    "Analyze campaign performance",
]

OPERATIONS_TASKS = [
    "Update internal documentation",
    "Review vendor contract",
    "Prepare monthly report",
    "Improve onboarding checklist",
    "Audit system permissions",
]


def generate_tasks(
    conn,
    project_ids: list,
    section_map: dict,
    user_ids: list,
    config: dict,
):
    """
    Generate tasks for all projects.

    Args:
        conn: SQLite connection
        project_ids (list): Project IDs
        section_map (dict): project_id -> list of section_ids
        user_ids (list): User IDs
        config (dict): Configuration values

    Returns:
        List[str]: Generated task IDs
    """

    seed_everything(config["random_seed"])

    tasks_per_project = config["tasks_per_project"]
    history_days = config["history_days"]

    rows = []
    task_ids = []

    for project_id in project_ids:
        sections = section_map[project_id]

        for _ in range(tasks_per_project):
            task_id = str(uuid.uuid4())

            # Choose section (bias toward "To Do" / "In Progress")
            section_id = random.choices(
                sections,
                weights=[0.15, 0.35, 0.25, 0.15, 0.10],
                k=1
            )[0]

            # Choose task name based on project type (encoded in name heuristics)
            project_type_hint = random.random()
            if project_type_hint < 0.5:
                name = random.choice(ENGINEERING_TASKS)
            elif project_type_hint < 0.8:
                name = random.choice(MARKETING_TASKS)
            else:
                name = random.choice(OPERATIONS_TASKS)

            description = (
                f"This task involves: {name.lower()}.\n\n"
                f"Acceptance criteria:\n"
                f"- Requirements implemented\n"
                f"- Verified and reviewed"
                if probability(0.6)
                else None
            )

            created_at = random_past_datetime(history_days)
            due_date = maybe_due_date()

            # 15% unassigned tasks
            assignee_id = (
                random.choice(user_ids)
                if probability(0.85)
                else None
            )

            # Completion logic
            completed = probability(0.65)
            completed_at = (
                completion_time(created_at).isoformat()
                if completed
                else None
            )

            rows.append(
                (
                    task_id,
                    project_id,
                    section_id,
                    assignee_id,
                    name,
                    description,
                    due_date,
                    completed,
                    created_at.isoformat(),
                    completed_at,
                )
            )

            task_ids.append(task_id)

    query = """
        INSERT INTO tasks (
            task_id,
            project_id,
            section_id,
            assignee_id,
            name,
            description,
            due_date,
            completed,
            created_at,
            completed_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    execute_many(conn, query, rows)

    logger.info(f"Generated {len(task_ids)} tasks")

    return task_ids
