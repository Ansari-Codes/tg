CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    pswd TEXT NOT NULL,
    avatar TEXT,
    role TEXT DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_PROJECTS_TABLE = """
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    owner INTEGER NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    description TEXT,
    pycode TEXT,
    jscode TEXT,
    likes INTEGER DEFAULT 0,
    status INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(owner) REFERENCES users(id)
);
"""

CREATE_COMMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    commentor INTEGER NOT NULL,
    project INTEGER NOT NULL,
    reply_to INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(commentor) REFERENCES users(id),
    FOREIGN KEY(project) REFERENCES projects(id),
    FOREIGN KEY(reply_to) REFERENCES comments(id)
);
"""

from db import RUN_SQL

async def CreateTables():
    await RUN_SQL(CREATE_USERS_TABLE)
    print("cli.py: created users table")
    await RUN_SQL(CREATE_PROJECTS_TABLE)
    print("cli.py: created projects table")
    await RUN_SQL(CREATE_COMMENTS_TABLE)
    print("cli.py: created comments table")

print("cli.py: Creating tables")
import asyncio
asyncio.run(CreateTables())
print("cli.py: Database initialized!")
