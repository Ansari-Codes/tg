import sqlite3 as sq

async def SQL(query: str, to_fetch=False):
    print(f"DevDB: Running\n\t", query)
    conn = sq.connect('database.sqlite')
    data = conn.execute(query).fetchall()
    conn.commit()
    print(f"DevDb: Ran!\n\t", data)
    return data
