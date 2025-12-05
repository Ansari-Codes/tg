# database/auth.py (relevant parts)
from db import RUN_SQL, USERS
from models import Response
from .helpers import  verifyMail, verifyPswd, verifyUsername, escapeSQL, isUnique

async def unique(item, col):
    return await isUnique(item, col, USERS)

async def insert_user(name, mail, pswd, avatar):
    query = f"""
    INSERT INTO {USERS} (name, email, pswd, avatar)
    VALUES ('{name}', '{mail}', '{pswd}', '{avatar}');
    """
    await RUN_SQL(query)
    fetch_query = f"""
    SELECT * FROM {USERS}
    WHERE name = '{name}' AND email = '{mail}';
    """
    row = await RUN_SQL(fetch_query, True)
    return row[0] if row else {}

async def signup(
    name: str,
    mail: str,
    pswd: str,
    avatar: str = "🐢",
) -> Response:
    """
    Signup flow:
     - validates username, mail, password
     - escapes quotes
     - inserts and returns inserted row via RUN_SQL
    """
    name = escapeSQL(name.strip().lower())
    mail = escapeSQL(mail.strip().lower())
    pswd = escapeSQL(pswd)
    res = Response()

    # --- validations (FIXED: pass correct variables) ---
    if not verifyUsername(name): res.errors['name'] = "Username can only contain letters and numbers."
    if not verifyMail(mail): res.errors['mail'] = "Invalid mail."
    if not verifyPswd(pswd): res.errors['pswd'] = "Password is not strong."
    if not await unique(name, 'name'):
        res.errors['name'] = "Username already taken!"
    if not await unique(mail, 'email'):
        res.errors['mail'] = "Email already taken!"
    if not res.success: return res
    res.data = await insert_user(name, mail, pswd, avatar)
    return res


