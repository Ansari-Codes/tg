import sqlite3 as sq
import aiosqlite as asq

DATABASE = "database.sqlite"

async def INIT_DB():
    con = await asq.connect(DATABASE)
    con.row_factory = sq.Row
    return con

async def SQL(query, params=(), fetch=False):
    con = await INIT_DB()
    try:
        async with con.execute(query, params) as cur:
            if fetch:
                rows = await cur.fetchall()
                return [dict(row) for row in rows]
            else:
                await con.commit()
                return True
    except Exception as e:
        return None
    finally:
        await con.close()
