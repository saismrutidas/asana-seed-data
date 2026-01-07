import uuid
import random

from loguru import logger

from utils.db import execute_many
from utils.random import seed_everything, probability


CUSTOM_FIELD_TEMPLATES = {
    "engineering": [
        ("Priority", "enum", ["P0", "P1", "P2", "P3"]),
        ("Story Points", "number", None),
    ],
    "marketing": [
        ("Channel", "enum", ["Email", "SEO", "Paid Ads", "Social"]),
        ("Budget ($)", "number", None),
    ],
    "operations": [
        ("Owner Approval", "enum", ["Yes", "No"]),
        ("Risk Level", "enum", ["Low", "Medium", "High"]),
    ],
}


def generate_custom_fields(
    conn,
    project_ids: list,
    task_ids: list,
    config: dict = None,
):
    """
    Generate custom fields per project and assign values to tasks.

    Args:
        conn: SQLite connection
        project_ids (list): Project IDs
        task_ids (list): Task IDs
        config (dict, optional): Configuration values
    """

    if config and "random_seed" in config:
        seed_everything(config["random_seed"])

    field_rows = []
    value_rows = []

    # Create custom fields per project
    project_field_map = {}

    for project_id in project_ids:
        # Randomly assign a project type for field selection
        project_type = random.choices(
            ["engineering", "marketing", "operations"],
            weights=[0.5, 0.3, 0.2],
            k=1
        )[0]

        project_field_map[project_id] = []

        for field_name, field_type, enum_values in CUSTOM_FIELD_TEMPLATES[project_type]:
            field_id = str(uuid.uuid4())

            field_rows.append(
                (
                    field_id,
                    project_id,
                    field_name,
                    field_type,
                )
            )

            project_field_map[project_id].append(
                (field_id, field_type, enum_values)
            )

    field_query = """
        INSERT INTO custom_fields (
            field_id,
            project_id,
            name,
            field_type
        )
        VALUES (?, ?, ?, ?)
    """

    execute_many(conn, field_query, field_rows)

    # Assign custom field values to tasks (sparse)
    for project_id, fields in project_field_map.items():
        relevant_tasks = random.sample(
            task_ids,
            k=max(1, int(0.2 * len(task_ids)))
        )

        for task_id in relevant_tasks:
            for field_id, field_type, enum_values in fields:
                if not probability(0.6):
                    continue

                if field_type == "number":
                    value = str(random.randint(1, 13))
                elif field_type == "enum":
                    value = random.choice(enum_values)
                else:
                    value = "N/A"

                value_rows.append(
                    (
                        field_id,
                        task_id,
                        value,
                    )
                )

    value_query = """
        INSERT INTO custom_field_values (
            field_id,
            task_id,
            value
        )
        VALUES (?, ?, ?)
    """

    execute_many(conn, value_query, value_rows)

    logger.info(
        f"Generated {len(field_rows)} custom fields and "
        f"{len(value_rows)} custom field values"
    )
