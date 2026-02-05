from db import RUN_SQL, PROJECTS, USERS
from models import Response
from .helpers import isUnique, escapeSQL, randomstr, rnd
from typing import Literal

async def getPaginated(
    per_page: int = 100,
    page=1,
    search_q=None,
    orderBy: Literal["likes", "created_at"] = "likes",
    asc=False
):
    res = Response()

    # -------------------------------
    # Build WHERE conditions cleanly
    # -------------------------------
    conditions = ["p.status = 1"]   # always active

    if search_q:
        sq = escapeSQL(search_q)
        conditions.append(
            f"(p.title LIKE '%{sq}%' OR p.description LIKE '%{sq}%' "
            f"OR '{sq}' LIKE '%' || p.title || '%')"
        )

    # Compile WHERE clause
    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    # -------------------------------
    # Order direction
    # -------------------------------
    order_dir = "ASC" if asc else "DESC"

    # -------------------------------
    # Pagination
    # -------------------------------
    limit_clause = ""
    if isinstance(per_page, (int, float)):
        per_page = int(per_page)
        page = max(page, 1)
        offset = (page - 1) * per_page
        limit_clause = f"LIMIT {per_page} OFFSET {offset}"

    # -------------------------------
    # Main Query
    # -------------------------------
    query = f"""
        SELECT 
            p.*,
            u.id    AS owner_id,
            u.name  AS owner_name,
            u.email AS owner_email,
            u.avatar AS owner_avatar
        FROM {PROJECTS} AS p
        LEFT JOIN {USERS} AS u ON p.owner = u.id
        {where_clause}
        ORDER BY p.{orderBy} {order_dir}
        {limit_clause};
    """

    try:
        projects = await RUN_SQL(query, to_fetch=True)
    except Exception as e:
        print("Pagination error:", e)
        res.errors['project'] = "Cannot fetch projects!"
        return res
    if projects is None:
        res.errors['project'] = "Cannot fetch projects!"
        res.data = []
        return res
    # -------------------------------
    # Response structure
    # -------------------------------
    res.data = projects
    res.meta = {
        "per_page": per_page,
        "page": page,
    }
    return res
