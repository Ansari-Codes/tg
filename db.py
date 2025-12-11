import httpx
from devdb import SQL
import os
from dotenv import load_dotenv

# Load .env variables automatically
load_dotenv()  

API_URL = os.getenv("API_URL","")
PASSWORD = os.getenv("PASSWORD","")
print(API_URL, PASSWORD)
if not (API_URL or PASSWORD):
    raise Exception("API_URL Or PASSWORD didn't load!")
q = 0

USERS = "users"
PROJECTS = "projects"
COMMENTS = "comments"
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
    except httpx.HTTPStatusError as e: raise
    except httpx.RequestError as e: raise
    except Exception as e: raise
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
    for table in tables:
        await RUN_SQL(f"DELETE FROM `{table.get('name')}`;")

async def DROP():
    print("cli.py: Dropping tables...")
    DROP_COMMENTS = "DROP TABLE IF EXISTS comments;"
    DROP_PROJECTS = "DROP TABLE IF EXISTS projects;"
    DROP_USERS = "DROP TABLE IF EXISTS users;"
    drop = DROP_COMMENTS + DROP_PROJECTS + DROP_USERS
    await RUN_SQL(drop)
    print("cli.py: All tables dropped successfully!")

# import asyncio
# asyncio.run(DROP())
import asyncio

async def test_file_functions():
    filename = "test.txt"
    content = "Hello world!"

    # 1. POST (create/update file)
    msg = await POST_FILE(filename, content)
    print("POST_FILE:", msg)

    # 2. GET (read file)
    result = await GET_FILE(filename)
    print("GET_FILE:", result)

    # 3. DELETE (remove file)
    msg = await DELETE_FILE(filename)
    print("DELETE_FILE:", msg)

    # 4. GET after delete → should raise Exception
    try:
        await GET_FILE(filename)
    except Exception as e:
        print("GET_FILE after delete:", e)

asyncio.run(test_file_functions())
