from db import SESSIONS, RUN_SQL, USERS
from models import Response

async def getCurrentUser(token):
    res = Response()
    if not token:
        res.errors["ad"] = "as"
        return res
    try:
        session = await RUN_SQL(f"SELECT * FROM {SESSIONS} WHERE session_token='{token}';")
        print("getCurrectUser: ", session)
        if session:
            id  = session[0].get("user")
            if not id:
                res.errors['id'] = "Cannot fetch the user!"
                return res
            user = await RUN_SQL(f"SELECT * FROM {USERS} WHERE id={id};")
            res.data = user[0] if user else {}
            return res
        else:
            res.errors['session'] = "Cannot find session!"
            return res
    except Exception as e:
        res.errors["other"] = str(e)
        return res
