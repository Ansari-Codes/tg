from db import RUN_SQL, PROJECTS, USERS, LIKEDS, VIEWEDS
from models import Response
from .helpers import isUnique, escapeSQL, randomstr, rnd

async def unique(item, col):
    return await isUnique(item, col, PROJECTS)

async def createEmtpyProject(id):
    res = Response()
    if not res.success:return res
    title = randomstr()
    try:
        if not (await unique(title, 'title')):
            title = randomstr(8)
    except Exception as e:
        res.errors['project'] = "Unable to create project!"
    owner = id
    slug = randomstr()
    pycode = "print('Turtle graphics')"
    jscode = "console.log('Turtle graphics')"
    likes = str(0)
    views = str(0)
    description = ""
    query = f"""
    INSERT INTO {PROJECTS} ( title , owner , slug , pycode , jscode , likes , description , views )
    VALUES ('{escapeSQL(title)}', '{escapeSQL(owner)}', '{escapeSQL(slug)}', '{escapeSQL(pycode)}', '{escapeSQL(jscode)}', '{escapeSQL(likes)}', '{escapeSQL(description)}', '{escapeSQL(views)}');
    """
    try:
        await RUN_SQL(query)
    except Exception as e:
        res.errors['other'] = "Unable to create project!"
        return res
    fetch_query = f"""
    SELECT * FROM {PROJECTS} WHERE slug = '{escapeSQL(slug)}';
    """
    try:
        row = await RUN_SQL(fetch_query, True)
    except Exception as e:
        res.errors['other'] = "Unable to create project!"
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
        return res
    res.data = projects
    return res

async def loadProject(item, by="slug", owner=None, withowner=True):
    res = Response()
    value = escapeSQL(str(item))
    value = f"'{value}'"
    if withowner: oo = "AND owner = " + str(owner)
    else: oo=""
    query = f"""
    SELECT *
    FROM {PROJECTS}
    WHERE {by} = {value} {oo}
    ORDER BY id DESC
    LIMIT 1;
    """
    try:
        project = await RUN_SQL(query, True)
    except Exception as e:
        res.errors['project'] = "Cannot load project!"
        return res
    if project and project[0]:
        prjt = project[0]
        dict(prjt).pop("views", "")
        dict(prjt).pop("likes", "")
        res.data = project[0]
    else:
        res.data = {}
        res.errors["project"] = "Project not found"
    return res

async def loadProjectWithOwner(item, by="slug"):
    res = Response()
    value = escapeSQL(str(item))
    value = f"'{value}'"

    query = f"""
    SELECT p.*, 
        u.id AS owner_id, 
        u.name AS owner_name, 
        u.email AS owner_email, 
        u.avatar AS owner_avatar
    FROM {PROJECTS} AS p
    LEFT JOIN {USERS} AS u
        ON p.owner = u.id
    WHERE p.{by} = {value}
    ORDER BY p.id DESC
    LIMIT 1;
    """
    try:
        project = await RUN_SQL(query, True)
    except Exception as e:
        res.errors['project'] = "Cannot load project!"
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
        return res
    res.data = row[0] if row else {}
    return res

async def deleteProject(id):
    res = Response()
    try:
        await RUN_SQL(f"DELETE FROM {PROJECTS} WHERE id = {id};")
    except Exception as e:
        res.errors['error'] = str(e)
    return res

async def likeAProject(project_id, liker_id):
    res = Response()
    if not project_id:
        res.errors['project_id'] = "project_id is required"
    if not liker_id:
        res.errors['liker_id'] = "liker_id is required"
    if not res.success:return res
    try:
        query_check = f"""
        SELECT 1 FROM {LIKEDS}
        WHERE project_id = {project_id} AND liker_id = {liker_id}
        LIMIT 1;
        """
        existing = await RUN_SQL(query_check, to_fetch=True)
        if existing:
            query_del = f"""
            DELETE FROM {LIKEDS}
            WHERE project_id = {project_id} AND liker_id = {liker_id};
            """
            await RUN_SQL(query_del)
            query_update = f"""
            UPDATE {PROJECTS}
            SET likes = likes - 1
            WHERE id = {project_id} AND likes > 0;
            """
            await RUN_SQL(query_update)
            action = "disliked"
        else:
            query_insert = f"""
            INSERT INTO {LIKEDS} (project_id, liker_id)
            VALUES ({project_id}, {liker_id});
            """
            await RUN_SQL(query_insert)
            query_update = f"""
            UPDATE {PROJECTS}
            SET likes = likes + 1
            WHERE id = {project_id};
            """
            await RUN_SQL(query_update)
            action = "liked"
        query2 = f"SELECT likes FROM {PROJECTS} WHERE id = {project_id}"
        updated = await RUN_SQL(query2, to_fetch=True)
        res.data = {
            "id": project_id,
            "likes": updated[0]["likes"] if updated else 0,
            "action": action
        }
    except Exception as e:
        res.errors["like"] = "Cannot like project"
    return res

async def hasLiked(project_id, liker_id):
    res = Response()
    if not project_id:
        res.errors['project_id'] = "project_id is required"
    if not liker_id:
        res.errors['liker_id'] = "liker_id is required"
    if not res.success:return res
    try:
        query_check = f"""
        SELECT 1 FROM {LIKEDS}
        WHERE project_id = {project_id} AND liker_id = {liker_id}
        LIMIT 1;
        """
        existing = await RUN_SQL(query_check, to_fetch=True)
        if existing:
            res.data = existing[0]
            return res
        else:
            res.data = {}
            return res
    except Exception as e:
        res.errors['error'] = str(e)
        return res

async def viewAProject(project_id, viewer_id):
    res = Response()
    if not project_id:
        res.errors['project_id'] = "project_id is required"
    if not viewer_id:
        res.errors['viewer_id'] = "viewer_id is required"
    if not res.success:return res
    try:
        query_check = f"""
        SELECT 1 FROM {VIEWEDS}
        WHERE project_id = {project_id} AND viewer_id = {viewer_id}
        LIMIT 1;
        """
        existing = await RUN_SQL(query_check, to_fetch=True)
        if existing:
            res.meta['view'] = "already viewed"
            return res
        else:
            query_insert = f"""
            INSERT INTO {VIEWEDS} (project_id, viewer_id)
            VALUES ({project_id}, {viewer_id});
            """
            await RUN_SQL(query_insert)
            query_update = f"""
            UPDATE {PROJECTS}
            SET views = views + 1
            WHERE id = {project_id};
            """
            await RUN_SQL(query_update)
        query2 = f"SELECT views FROM {PROJECTS} WHERE id = {project_id}"
        updated = await RUN_SQL(query2, to_fetch=True)
        res.data = {
            "id": project_id,
            "views": updated[0]["views"] if updated else 0,
        }
    except Exception as e:
        res.errors["view"] = "Cannot view project"

    return res
