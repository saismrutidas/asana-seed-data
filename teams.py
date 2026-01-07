import uuid
import random
from datetime import datetime

from loguru import logger

from utils.db import execute_many
from utils.random import seed_everything


TEAM_NAME_POOL = [
    "Platform Engineering",
    "Frontend Engineering",
    "Backend Engineering",
    "Infrastructure",
    "DevOps",
    "Quality Assurance",
    "Product Management",
    "Design",
    "Growth Marketing",
    "Content Marketing",
    "Sales Operations",
    "Customer Success",
    "Revenue Operations",
    "Business Operations",
    "Finance",
    "HR Operations",
    "IT Support",
]


def generate_teams(conn, org_id: str, user_ids: list, config: dict):
    """
    Generate teams and team memberships.

    Args:
        conn: SQLite connection
        org_id (str): Organization ID
        user_ids (list): List of user IDs
        config (dict): Configuration values

    Returns:
        List[str]: Generated team IDs
    """

    seed_everything(config["random_seed"])

    num_teams = config["num_teams"]
    created_at = datetime.utcnow().isoformat()

    teams = []
    memberships = []
    team_ids = []

    # Pick team names (reuse if num_teams > pool size)
    for i in range(num_teams):
        team_id = str(uuid.uuid4())
        name = TEAM_NAME_POOL[i % len(TEAM_NAME_POOL)]

        teams.append(
            (
                team_id,
                org_id,
                name,
                created_at
            )
        )
        team_ids.append(team_id)

        # Assign users to teams
        # Each team has 10–30% of total users
        team_size = random.randint(
            int(0.10 * len(user_ids)),
            int(0.30 * len(user_ids))
        )

        members = random.sample(user_ids, team_size)

        for user_id in members:
            memberships.append((team_id, user_id))

    team_query = """
        INSERT INTO teams (team_id, org_id, name, created_at)
        VALUES (?, ?, ?, ?)
    """

    membership_query = """
        INSERT INTO team_memberships (team_id, user_id)
        VALUES (?, ?)
    """

    execute_many(conn, team_query, teams)
    execute_many(conn, membership_query, memberships)

    logger.info(
        f"Generated {len(team_ids)} teams and "
        f"{len(memberships)} team memberships"
    )

    return team_ids
