# database/auth.py (relevant parts)
from db import RUN_SQL
from string import ascii_letters, digits, punctuation
from models import Response
import re

def verifyUsername(name: str):
    if not name:
        return False
    for i in name:
        if i not in digits + ascii_letters:
            return False
    return True

def verifyMail(mail: str):
    return re.match(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        mail
    ) is not None

def verifyPswd(password: str) -> bool:
    strength = 0
    strength += any(c.isalpha() for c in password)
    strength += any(c in punctuation for c in password)
    strength += any(c.isdigit() for c in password)
    strength += (len(password) >= 8)
    return strength == 4

async def isUnique(item, col):
    query = f"SELECT COUNT(*) FROM users WHERE {col} = '{item}';"
    selected = await RUN_SQL(query,True)
    return not bool(selected[0] if selected else 0)

def _escape_sql(s: str) -> str:
    """Simple quote-escape for embedding into SQL strings (for RUN_SQL)."""
    return s.replace("'", "''")

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
    name = name.strip().lower()
    mail = mail.strip().lower()
    res = Response()

    # --- validations (FIXED: pass correct variables) ---
    if not verifyUsername(name): res.errors['name'] = "Username can only contain letters and numbers."
    if not verifyMail(mail): res.errors['mail'] = "Invalid mail."
    if not verifyPswd(pswd): res.errors['pswd'] = "Password is not strong."
    if not await isUnique(name, 'name'):
        res.errors['name'] = "Username already taken!"
    if not await isUnique(mail, 'email'):
        res.errors['mail'] = "Email already taken!"
    if not res.success: return res

    # --- escape values for safe embedding into SQL string ---
    name_esc = _escape_sql(name)
    mail_esc = _escape_sql(mail)
    pswd_esc = _escape_sql(pswd)
    avatar_esc = _escape_sql(avatar)

    query = f"""
    INSERT INTO users (name, email, pswd, avatar)
    VALUES ('{name_esc}', '{mail_esc}', '{pswd_esc}', '{avatar_esc}')
    RETURNING *;
    """
    inserted = await RUN_SQL(query, to_fetch=True)
    res.data = inserted[0]
    return res


