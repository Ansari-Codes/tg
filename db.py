import httpx
API_URL = "http://worldofansari.com/dbapi"
q = 0
async def RUN_SQL(query: str, to_fetch: bool = False):
    global q
    payload = {"query": query, "to_fetch": to_fetch, "name": "turtlegraphics"}
    q += 1
    print(f"DB: {q}: Running\n\t", query)
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(API_URL, json=payload)
            response.raise_for_status()
            return response.json().get("data", [{}])
    except httpx.HTTPStatusError as e: raise
    except httpx.RequestError as e: raise
    except Exception as e: raise
    finally: print(f"DB: {q}: Query ran!")

async def CLEAR():
    tables = await RUN_SQL("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%';
    """, to_fetch=True)
    for table in tables:
        await RUN_SQL(f"DELETE FROM `{table.get('name')}`;")
