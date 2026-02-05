import httpx
import os
from dotenv import load_dotenv
from ENV import app

API_URL = os.getenv("API_URL", "")
PASSWORD = os.getenv("PASSWORD", "")
if not (API_URL and PASSWORD):
    raise Exception("API_URL or PASSWORD didn't load!")

# ---- CONSTANTS ----
USERS = "users"
SESSIONS = "sessions"
PROJECTS = "projects"
COMMENTS = "comments"
LIKEDS = "likeds"
VIEWEDS = "vieweds"

name = "turtlegraphics"

# ---- FAST GLOBAL CLIENT ----
client = httpx.AsyncClient(
    timeout=httpx.Timeout(
        connect=5.0,
        read=10.0,
        write=10.0,
        pool=5.0
    ),
    limits=httpx.Limits(
        max_connections=50,
        max_keepalive_connections=20,
        keepalive_expiry=30
    ),
    http2=True
)

# ---- INTERNAL POST HELPER ----
async def _post(payload: dict):
    response = await client.post(API_URL, json=payload)
    response.raise_for_status()
    res = response.json()
    if not res.get("success"):
        raise Exception(res.get("error"))
    return res


# ===================== DB =====================
q = 0

async def RUN_SQL(query: str, to_fetch: bool = False):
    global q
    q += 1
    payload = {
        "query": query,
        "to_fetch": to_fetch,
        "name": name,
        "password": PASSWORD,
        "purpose": "db"
    }
    try:
        res = await _post(payload)
        return res.get("data", [{}])
    except Exception as e:
        print(e)


async def rawRUN_SQL(query: str, to_fetch: bool = True):
    payload = {
        "query": query,
        "to_fetch": to_fetch,
        "name": name,
        "password": PASSWORD,
        "purpose": "db"
    }
    return await _post(payload)


# ===================== FILE =====================
f = 0

async def GET_FILE(file: str):
    global f
    f += 1
    print(f"FILE[{f}] → GET {file}")

    payload = {
        "name": name,
        "file": file,
        "password": PASSWORD,
        "purpose": "file",
        "todo": "get"
    }

    res = await _post(payload)
    return res.get("content", "")


async def POST_FILE(file: str, content: str):
    global f
    f += 1
    print(f"FILE[{f}] → POST {file}")

    payload = {
        "name": name,
        "file": file,
        "content": content,
        "password": PASSWORD,
        "purpose": "file",
        "todo": "post"
    }

    res = await _post(payload)
    return res.get("message", "")


async def DELETE_FILE(file: str):
    global f
    f += 1
    print(f"FILE[{f}] → DELETE {file}")

    payload = {
        "name": name,
        "file": file,
        "password": PASSWORD,
        "purpose": "file",
        "todo": "delete"
    }

    res = await _post(payload)
    return res.get("message", "")


# ===================== UTILS =====================
async def CLEAR():
    tables = await RUN_SQL("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%';
    """, to_fetch=True)

    for table in tables:  # type: ignore
        await RUN_SQL(f"DELETE FROM `{table.get('name')}`;")


async def DROP():
    print("cli.py: Dropping tables...")
    drop = "\n".join([
        "DROP TABLE IF EXISTS comments;",
        "DROP TABLE IF EXISTS projects;",
        "DROP TABLE IF EXISTS users;",
        "DROP TABLE IF EXISTS sessions;",
        "DROP TABLE IF EXISTS likeds;",
        "DROP TABLE IF EXISTS vieweds;"
    ])
    await RUN_SQL(drop)
    print("cli.py: All tables dropped successfully!")


# ===================== SHUTDOWN =====================
async def CLOSE():
    await client.aclose()

app.on_shutdown(CLOSE)
