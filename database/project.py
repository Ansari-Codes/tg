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
    VALUES ('{escapeSQL(title)}', '{escapeSQL(owner)}', '{escapeSQL(slug)}', 
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

async def getAllProjects(item: int|str, by="owner"):
    res = Response()
    projects = await RUN_SQL(f"""
    SELECT * FROM {PROJECTS} WHERE {by} = {escapeSQL(item)};
    """, True)
    res.data = projects
    return res

async def loadProject(item, by="slug"):
    res = Response()
    value = escapeSQL(str(item))
    value = f"'{value}'"
    query = f"""
    SELECT *
    FROM {PROJECTS}
    WHERE {by} = {value}
    ORDER BY id DESC
    LIMIT 1;
    """
    project = await RUN_SQL(query, True)
    if project and project[0]:
        res.data = project[0]
    else:
        res.data = {}
        res.errors["project"] = "Project not found"
    return res
