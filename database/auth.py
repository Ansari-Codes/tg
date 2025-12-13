# database/auth.py (relevant parts)
from db import RUN_SQL, USERS
from models import Response
from .helpers import  verifyMail, verifyPswd, verifyUsername, escapeSQL, isUnique
from devdb import SQL
async def unique(item, col):
    return await isUnique(item, col, USERS)

async def insert_user(name, mail, pswd, avatar):
    query = f"""
    INSERT INTO {USERS} ( name , email , pswd , avatar )
    VALUES ('{name}', '{mail}', '{pswd}', '{avatar}');
    """
    await RUN_SQL(query)
    fetch_query = f"""
    SELECT * FROM {USERS}
    WHERE name = '{name}' AND email = '{mail}';
    """
    row = await RUN_SQL(fetch_query, True)
    print("insert_user: ", row)
    return row[0] if row else {}

async def signup(
    name: str,
    mail: str,
    pswd: str,
    avatar: str = "🐢",
) -> Response:
    name = escapeSQL(name.strip().lower())
    mail = escapeSQL(mail.strip().lower())
    pswd = escapeSQL(pswd)
    res = Response()

    # --- validations (FIXED: pass correct variables) ---
    if not verifyUsername(name): res.errors['name'] = "Username can only contain letters and numbers."
    if not verifyMail(mail): res.errors['mail'] = "Invalid mail."
    if not verifyPswd(pswd): res.errors['pswd'] = "Password is not strong."
    try:
        if not await unique(name, 'name'):
            res.errors['name'] = "Username already taken!"
        else:
            print("Username is valid")
        if not await unique(mail, 'email'):
            res.errors['mail'] = "Email already taken!"
        else:
            print("Mail is valid")
        if not res.success: return res
        else:
            print("Succeeded")
        res.data = await insert_user(name, mail, pswd, avatar)
    except Exception as e:
        res.errors['other'] = "Cannot create account!"
        print(e)
        return res
    print(res.data)
    return res

async def login(iden:str, pswd:str)->Response:
    iden = escapeSQL(iden.strip().lower())
    pswd = pswd
    res = Response()
    query = f"""
    SELECT * FROM {USERS}
    WHERE name = '{iden}' OR email = '{iden}';
    """
    try:
        result = await RUN_SQL(query, True)
    except Exception as e:
        res.errors['acc'] = "Unable to login"
        print(e)
        return res
    print("Login:", result)
    if result and result[0]:
        data = result[0]
        if data.get("pswd") == pswd:
            res.data = data
            return res
        else:
            res.errors["acc"] = "Password is incorrect!"
    else: res.errors["acc"] = "Account not found!"
    return res
