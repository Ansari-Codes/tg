from db import RUN_SQL, PROJECTS, USERS
from models import Response
from .helpers import isUnique, escapeSQL, randomstr, rnd
from database.project import getAllProjectsWithoutPaginationOrSearch

async def getUser(item, by='id'):
    res = Response()
    try:
        itm = escapeSQL(f"{item}") if isinstance(item, str) else item
        resp = await RUN_SQL(f"SELECT * FROM {USERS} WHERE {by} = {itm}", True)
    except Exception as e:
        res.errors['user'] = e
        return res
    res.data = resp[0] if resp else {}
    return res

async def getUserName(item, by='id'):
    res = Response()
    try:
        itm = escapeSQL(f"{item}") if isinstance(item, str) else item
        resp = await RUN_SQL(f"SELECT name FROM {USERS} WHERE {by} = {itm}", True)
    except Exception as e:
        res.errors['user'] = e
        return res
    res.data = resp[0] if resp else {}
    return res

async def countProjects(item, by='owner'):
    res = Response()
    try:
        itm = escapeSQL(f"{item}") if isinstance(item, str) else item
        query = f"""
            SELECT 
                COUNT(*) AS total,
                SUM(likes) AS lks,
                SUM(views) AS vws,
                SUM(CASE WHEN status = 0 THEN 1 ELSE 0 END) AS drafts,
                SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) AS publics
            FROM {PROJECTS}
            WHERE {by} = {itm};
        """
        resp = await RUN_SQL(query, to_fetch=True)
    except Exception as e:
        res.errors['user'] = "Cannot fetch data!"
        return res
    if resp and len(resp) > 0:
        row = resp[0]
        res.data = {
            "projs": row.get("total", 0),
            "draft": row.get("drafts", 0),
            "pubs": row.get("publics", 0),
            "likes": row.get("lks", 0),
            "views": row.get("vws", 0),
        }
    else:
        res.data = {"projs": 0, "draft": 0, "pubs": 0, "likes": 0, "views": 0}
    return res

async def getLatestProjects(owner, count=5):
    res = Response()
    query = f"SELECT * FROM {PROJECTS} WHERE owner = {owner} ORDER BY updated_at DESC LIMIT {count};"
    try:
        projects = await RUN_SQL(query, to_fetch=True)
    except Exception as e:
        res.errors['project'] = "Cannot fetch projects!"
        return res
    res.data = projects
    return res

async def getDataForGraph(limit: int = 50):
    res = Response()
    query = f"""
        SELECT 
            title,
            likes,
            slug
        FROM {PROJECTS}
        WHERE status = 1
        ORDER BY updated_at DESC
        LIMIT {int(limit)};
    """
    try:
        data = await RUN_SQL(query, to_fetch=True)
    except Exception as e:
        res.errors["graph"] = "Cannot fetch graph data!"
        return res
    res.data = data #type:ignore
    return res
