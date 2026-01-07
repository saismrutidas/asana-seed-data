import uuid
from datetime import datetime

from loguru import logger

from utils.db import execute_one


def generate_organization(conn):
    """
    Generate a single organization/workspace.

    Returns:
        org_id (str): UUID of the created organization
    """

    org_id = str(uuid.uuid4())

    org_name = "Acme Cloud Technologies"
    domain = "acmecloud.com"
    created_at = datetime.utcnow().isoformat()

    query = """
        INSERT INTO organizations (org_id, name, domain, created_at)
        VALUES (?, ?, ?, ?)
    """

    execute_one(
        conn,
        query,
        (org_id, org_name, domain, created_at)
    )

    logger.info(f"Organization created: {org_name} ({org_id})")

    return org_id
