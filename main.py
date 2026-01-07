import os
import sqlite3
import sys
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

# Add src/ to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))


def load_config():
    """Load and validate environment variables."""
    load_dotenv()

    config = {
        "db_path": os.getenv("DB_PATH", "output/asana_simulation.sqlite"),
        "num_users": int(os.getenv("NUM_USERS", 500)),
        "num_teams": int(os.getenv("NUM_TEAMS", 25)),
        "projects_per_team": int(os.getenv("PROJECTS_PER_TEAM", 4)),
        "tasks_per_project": int(os.getenv("TASKS_PER_PROJECT", 120)),
        "subtask_ratio": float(os.getenv("SUBTASK_RATIO", 0.3)),
        "history_days": int(os.getenv("HISTORY_DAYS", 180)),
        "random_seed": int(os.getenv("RANDOM_SEED", 42)),
    }

    return config


def init_database(db_path: str):
    """Create SQLite database and execute schema.sql."""
    logger.info("Initializing SQLite database")

    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")

    schema_file = BASE_DIR.parent / "schema.sql"
    if not schema_file.exists():
        raise FileNotFoundError("schema.sql not found")

    with open(schema_file, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    return conn


def main():
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    try:
        config = load_config()
        logger.info("Configuration loaded")

        conn = init_database(config["db_path"])
        logger.info("Database schema created")

        # Import generators lazily (after DB is ready)
        from generators.organizations import generate_organization
        from generators.users import generate_users
        from generators.teams import generate_teams
        from generators.projects import generate_projects
        from generators.sections import generate_sections
        from generators.tasks import generate_tasks
        from generators.subtasks import generate_subtasks
        from generators.tags import generate_tags
        from generators.comments import generate_comments
        from generators.custom_fields import generate_custom_fields

        # Generation pipeline
        org_id = generate_organization(conn)
        user_ids = generate_users(conn, org_id, config)
        team_ids = generate_teams(conn, org_id, user_ids, config)
        project_ids = generate_projects(conn, team_ids, config)
        # section_ids = generate_sections(conn, project_ids)
        # task_ids = generate_tasks(conn, project_ids, section_ids, user_ids, config)
        section_map = generate_sections(conn, project_ids)
        task_ids = generate_tasks(
            conn,
            project_ids,
            section_map,
            user_ids,
            config
        )

        generate_subtasks(conn, task_ids, user_ids, config)
        generate_tags(conn, task_ids)
        generate_comments(conn, task_ids, user_ids)
        generate_custom_fields(conn, project_ids, task_ids)

        conn.commit()
        conn.close()

        logger.success("Asana simulation database generated successfully")

    except Exception as e:
        logger.exception("Database generation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
