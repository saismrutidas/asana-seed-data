import uuid
import random
from datetime import datetime

from loguru import logger

from utils.db import execute_many
from utils.dates import random_past_datetime, random_future_date
from utils.random import seed_everything


ENGINEERING_PROJECTS = [
    "Core Platform Refactor",
    "Authentication Service Improvements",
    "API Performance Optimization",
    "Mobile App Stability Sprint",
    "Observability & Monitoring Upgrade",
    "Billing System Revamp",
]

MARKETING_PROJECTS = [
    "Q2 Product Launch Campaign",
    "Website SEO Improvements",
    "Customer Case Study Program",
    "Email Nurture Campaign",
    "Brand Refresh Initiative",
]

OPERATIONS_PROJECTS = [
    "Internal Tooling Improvements",
    "Hiring Pipeline Optimization",
    "Compliance & Security Review",
    "Customer Support Workflow Update",
    "Quarterly Planning & OKRs",
]


def generate_projects(conn, team_ids: list, config: dict):
    """
    Generate projects for each team.

    Args:
        conn: SQLite connection
        team_ids (list): List of team IDs
        config (dict): Configuration values

    Returns:
        List[str]: Generated project IDs
    """

    seed_everything(config["random_seed"])

    projects_per_team = config["projects_per_team"]
    history_days = config["history_days"]

    rows = []
    project_ids = []

    for team_id in team_ids:
        for _ in range(projects_per_team):
            project_id = str(uuid.uuid4())

            project_type = random.choices(
                ["engineering", "marketing", "operations"],
                weights=[0.5, 0.3, 0.2],
                k=1
            )[0]

            if project_type == "engineering":
                name = random.choice(ENGINEERING_PROJECTS)
            elif project_type == "marketing":
                name = random.choice(MARKETING_PROJECTS)
            else:
                name = random.choice(OPERATIONS_PROJECTS)

            created_at = random_past_datetime(history_days).isoformat()

            # Not all projects have due dates
            due_date = (
                random_future_date(120)
                if random.random() < 0.7
                else None
            )

            rows.append(
                (
                    project_id,
                    team_id,
                    name,
                    project_type,
                    created_at,
                    due_date
                )
            )

            project_ids.append(project_id)

    query = """
        INSERT INTO projects (
            project_id,
            team_id,
            name,
            project_type,
            created_at,
            due_date
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """

    execute_many(conn, query, rows)

    logger.info(f"Generated {len(project_ids)} projects")

    return project_ids
