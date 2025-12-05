from db import RUN_SQL, PROJECTS
from models import Response
from .helpers import isUnique, escapeSQL, randomstr, rnd
from storage import getUserStorage

async def unique(item, col):
    return await isUnique(item, col, PROJECTS)

async def insertProject(title: str):
    owner = getUserStorage().get("id", 0)
    slug = (
        getUserStorage().get("name", randomstr())
        + randomstr()
        + str(rnd())
        + str(getUserStorage().get("id", rnd()))
    )
    pycode = "print('Turtle graphics')"
    jscode = "console.log('Turtle graphics')"
    likes = str(0)
    description = ""
    query = f"""
    INSERT INTO {PROJECTS} (title, owner, slug, pycode, jscode, likes, description)
    VALUES ('{escapeSQL(title)}', '{escapeSQL(str(owner))}', '{escapeSQL(slug)}', 
            '{escapeSQL(pycode)}', '{escapeSQL(jscode)}', '{escapeSQL(likes)}', '{escapeSQL(description)}');
    """
    await RUN_SQL(query)
    fetch_query = f"""
    SELECT * FROM {PROJECTS} WHERE slug = '{escapeSQL(slug)}';
    """
    row = await RUN_SQL(fetch_query, True)
    return row[0] if row else {}

async def createProject(title: str):
    title = escapeSQL(title.strip().lower()) if title.strip() else randomstr()
    res = Response()
    if not await unique(title, 'title'):
        res.errors['title']="Title already exists"
    if not res.success:return res
    res.data = await insertProject(title)
    return res

async def loadProject(item, by="slug"):
    query = f"""
    SELECT * FROM {PROJECTS} WHERE {by} = '{escapeSQL(str(item))}'
    """
    res = Response()
    res.data = ((await RUN_SQL(query, True)) or [{}])[0]
    return res

async def updateProject(item, by="slug", **updates):
    res = Response()
    if not updates:
        res.errors['updates'] = "No updates provided"
        return res
    allowed_cols = {"title", "description", "pycode", "jscode", "likes", "status", "updated_at"}
    set_clauses = []
    for col, val in updates.items():
        if col not in allowed_cols:
            continue
        set_clauses.append(f"{col} = '{escapeSQL(str(val))}'")
    if not set_clauses:
        res.errors['updates'] = "No valid columns to update"
        return res
    set_clauses.append("updated_at = CURRENT_TIMESTAMP")
    set_clause = ", ".join(set_clauses)
    query = f"""
    UPDATE {PROJECTS}
    SET {set_clause}
    WHERE {by} = '{escapeSQL(str(item))}';
    """
    await RUN_SQL(query)
    fetch_query = f"""
    SELECT * FROM {PROJECTS} WHERE {by} = '{escapeSQL(str(item))}';
    """
    row = await RUN_SQL(fetch_query, True)
    res.data = row[0] if row else {}
    return res

async def getProjects(owner):
    res = Response()
    fetch_query = f"""
    SELECT * FROM {PROJECTS} WHERE owner = '{escapeSQL(str(owner))}';
    """
    row = await RUN_SQL(fetch_query, True)
    print(row)
    res.data = row[0] if row else {}
    return res
