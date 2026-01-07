import uuid
from loguru import logger

from utils.db import execute_many


DEFAULT_SECTIONS = [
    "Backlog",
    "To Do",
    "In Progress",
    "In Review",
    "Done",
]


def generate_sections(conn, project_ids: list):
    """
    Generate workflow sections for each project.

    Args:
        conn: SQLite connection
        project_ids (list): List of project IDs

    Returns:
        Dict[str, List[str]]: Mapping of project_id -> section_ids
    """

    rows = []
    section_map = {}

    for project_id in project_ids:
        section_ids = []

        for position, name in enumerate(DEFAULT_SECTIONS, start=1):
            section_id = str(uuid.uuid4())

            rows.append(
                (
                    section_id,
                    project_id,
                    name,
                    position
                )
            )

            section_ids.append(section_id)

        section_map[project_id] = section_ids

    query = """
        INSERT INTO sections (
            section_id,
            project_id,
            name,
            position
        )
        VALUES (?, ?, ?, ?)
    """

    execute_many(conn, query, rows)

    logger.info(
        f"Generated sections for {len(project_ids)} projects"
    )

    return section_map
