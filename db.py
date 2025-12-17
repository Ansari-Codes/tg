import httpx
from devdb import SQL
import os
from dotenv import load_dotenv

# Load .env variables automatically
load_dotenv()  

API_URL = os.getenv("API_URL","")
PASSWORD = os.getenv("PASSWORD","")
if not (API_URL or PASSWORD):
    raise Exception("API_URL Or PASSWORD didn't load!")
q = 0

USERS = "users"
SESSIONS = "sessions"
PROJECTS = "projects"
COMMENTS = "comments"
LIKEDS = "likeds"
VIEWEDS = "vieweds"
name = "turtlegraphics"
async def RUN_SQL(query: str, to_fetch: bool = False):
    global q
    payload = {"query": query, "to_fetch": to_fetch, "name": name, "password":PASSWORD, "purpose":"db"}
    q += 1
    print(f"DB: {q}: Running\n\t", query)
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(API_URL, json=payload)
            response.raise_for_status()
            res = response.json()
            if res.get("success"): return res.get("data", [{}])
            else: raise Exception(res.get("error"))
        # return await SQL(query, to_fetch)
    except httpx.HTTPStatusError as e: raise
    except httpx.RequestError as e: raise
    except Exception as e: raise e
    finally: print(f"DB: {q}: Query ran!")
f = 0
async def GET_FILE(file):
    global f
    f+=1
    payload = {"name":name, "file":file, "password": PASSWORD, "purpose":"file", "todo":"get"}
    print(f"FILE: {f}: Running for `{file}`")
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(API_URL, json=payload)
            response.raise_for_status()
            res = response.json()
            if res.get("success"): return res.get("content", "")
            else: raise Exception(res.get("error"))
    except httpx.HTTPStatusError as e: raise
    except httpx.RequestError as e: raise
    except Exception as e: raise
    finally: print(f"FILE: {f}: Ran!")

async def POST_FILE(file, content):
    global f
    f+=1
    payload = {"name":name, "file":file, "content": content, "password": PASSWORD, "purpose":"file", "todo":"post"}
    print(f"FILE: {f}: Running for `{file}`")
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(API_URL, json=payload)
            response.raise_for_status()
            res = response.json()
            if res.get("success"): return res.get("message", "")
            else: raise Exception(res.get("error"))
    except httpx.HTTPStatusError as e: raise
    except httpx.RequestError as e: raise
    except Exception as e: raise
    finally: print(f"FILE: {f}: Ran!")

async def DELETE_FILE(file):
    global f
    f+=1
    payload = {"name":name, "file":file, "password": PASSWORD, "purpose":"file", "todo":"delete"}
    print(f"FILE: {f}: Running for `{file}`")
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(API_URL, json=payload)
            response.raise_for_status()
            res = response.json()
            if res.get("success"): return res.get("message", "")
            else: raise Exception(res.get("error"))
    except httpx.HTTPStatusError as e: raise
    except httpx.RequestError as e: raise
    except Exception as e: raise
    finally: print(f"FILE: {f}: Ran!")

async def CLEAR():
    tables = await RUN_SQL("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%';
    """, to_fetch=True)
    for table in tables:#type:ignore
        await RUN_SQL(f"DELETE FROM `{table.get('name')}`;")

async def DROP():
    print("cli.py: Dropping tables...")
    drop = '\n'.join([
        "DROP TABLE IF EXISTS comments;",
        "DROP TABLE IF EXISTS projects;",
        "DROP TABLE IF EXISTS users;",
        "DROP TABLE IF EXISTS sessions;",
        "DROP TABLE IF EXISTS likeds;",
        "DROP TABLE IF EXISTS vieweds;"
    ])
    await RUN_SQL(drop)
    print("cli.py: All tables dropped successfully!")

# import asyncio
# asyncio.run(DROP())
