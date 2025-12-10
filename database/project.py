from db import RUN_SQL, PROJECTS
from models import Response
from .helpers import isUnique, escapeSQL, randomstr, rnd
from storage import getUserStorage

async def unique(item, col):
    return await isUnique(item, col, PROJECTS)

async def createEmtpyProject():
    res = Response()
    if not res.success:return res
    title = randomstr()
    owner = getUserStorage().get("id", 0)
    slug = randomstr()
    pycode = "print('Turtle graphics')"
    jscode = "console.log('Turtle graphics')"
    likes = str(0)
    description = ""
    query = f"""
    INSERT INTO {PROJECTS} ( title , owner , slug , pycode , jscode , likes , description )
    VALUES ('{escapeSQL(title)}', '{escapeSQL(owner)}', '{escapeSQL(slug)}', '{escapeSQL(pycode)}', '{escapeSQL(jscode)}', '{escapeSQL(likes)}', '{escapeSQL(description)}');
    """
    try:
        await RUN_SQL(query)
    except Exception as e:
        res.errors['other'] = "Unable to create project!"
        print(e)
        return res
    fetch_query = f"""
    SELECT * FROM {PROJECTS} WHERE slug = '{escapeSQL(slug)}';
    """
    try:
        row = await RUN_SQL(fetch_query, True)
    except Exception as e:
        res.errors['other'] = "Unable to create project!"
        print(e)
        return res
    res.data = row[0] if row else {}
    return res

async def getAllProjects(
    item: int | str | None, 
    by="owner", 
    search_q: str = "", 
    per_page: int | None = 50, 
    page: int = 1
):
    res = Response()
    if not item:
        res.errors['project'] = "No identifier provided!"
        return res
    value = item if isinstance(item, (float, int)) else escapeSQL(item)
    where_clause = f"{by} = {value}"
    if search_q:
        sq = escapeSQL(search_q)
        where_clause += (
            f" AND (title LIKE '%{sq}%' OR description LIKE '%{sq}%' "
            f"OR '{sq}' LIKE '%' || title || '%')"
        )
    query = f"SELECT * FROM {PROJECTS} WHERE {where_clause}"
    if per_page is not None and isinstance(per_page, (float, int)):
        per_page = int(per_page)
        page = max(page, 1)
        offset = (page - 1) * per_page
        query += f" LIMIT {per_page} OFFSET {offset}"
    query += ";"
    try:
        projects = await RUN_SQL(query, to_fetch=True)
    except Exception as e:
        res.errors['project'] = "Cannot fetch projects!"
        print(e)
        return res
    res.data = projects
    res.meta = {
        "ppage": per_page,
        "page": page,
    }
    return res

async def getAllProjectsWithoutPaginationOrSearch(
    item: int | str | None, 
    by="owner", 
):
    res = Response()
    if not item:
        res.errors['project'] = "No identifier provided!"
        return res
    value = item if isinstance(item, (float, int)) else escapeSQL(item)
    where_clause = f"{by} = {value}"
    query = f"SELECT * FROM {PROJECTS} WHERE {where_clause}"
    query += ";"
    try:
        projects = await RUN_SQL(query, to_fetch=True)
    except Exception as e:
        res.errors['project'] = "Cannot fetch projects!"
        print(e)
        return res
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
    try:
        project = await RUN_SQL(query, True)
    except Exception as e:
        res.errors['project'] = "Cannot load project!"
        print(e)
        return res
    if project and project[0]:
        res.data = project[0]
    else:
        res.data = {}
        res.errors["project"] = "Project not found"
    return res

async def updateProject(data: dict):
    if 'id' not in data:
        raise KeyError("updateProject: Missing 'id' in incoming data")
    res = Response()
    data_copy = data.copy()
    project_id = data_copy.pop('id')
    set_clause = []
    for col, val in data_copy.items():
        if val is None:set_clause.append(f"{col} = NULL")
        elif isinstance(val, (int, float)): set_clause.append(f"{col} = {val}")
        else:set_clause.append(f"{col} = '{escapeSQL(str(val))}'")
    try:
        query = f"UPDATE {PROJECTS} SET {', '.join(set_clause)}, updated_at = CURRENT_TIMESTAMP WHERE id = {project_id};"
        await RUN_SQL(query)
        query = f"SELECT * FROM {PROJECTS} WHERE id = {project_id};"
        row = await RUN_SQL(query, True)
    except Exception as e:
        res.errors['project'] = "Cannot update project!"
        print(e)
        return res
    res.data = row[0] if row else {}
    return res
