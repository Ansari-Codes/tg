import sqlite3 as sq
import aiosqlite as asq

database = "database.sqlite"
async def INIT_DB():
    con = await asq.connect(database)
    cur = await con.cursor()
    cur.row_factory = sq.Row #type:ignore
    return con, cur

async def SQL(query="", to_fetch=False):
    con, cur = await INIT_DB()
    try:
        res = await cur.execute(query)
        if to_fetch:
            res = await res.fetchall()
            return [dict(row) for row in res]
    except Exception as e:
        print(e)
        return [{}]
    finally:
        await cur.close()
        await con.close()