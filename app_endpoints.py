from ENV import app
from fastapi.responses import Response
from fastapi.requests import Request
from uuid import uuid4
from db import RUN_SQL, SESSIONS
from datetime import datetime, timedelta, timezone
from database.dashb import getUser

async def saveCookie(value, userId, max_age):
    expires_at = (datetime.now(timezone.utc) + timedelta(seconds=max_age)).isoformat()
    try:
        await RUN_SQL(f"""INSERT INTO {SESSIONS} ( session_token , user , expires_at )
                    VALUES ( '{value}' , {userId}, '{expires_at}' )""")
        return True
    except Exception as e:
        return False

async def getCookie(userId: int, token: str):
    try:
        res = await RUN_SQL(
            f"SELECT * FROM {SESSIONS} WHERE user={userId} AND session_token='{token}';",
        )
        if res and res[0]:
            expires_at = datetime.fromisoformat(res[0]['expires_at'])
            if datetime.now(timezone.utc) > expires_at:
                return None, {}
            user = await getUser(userId)
            if user.success:
                user = user.data
                return True, user[0]
            else:
                return False, {}
        return False, {}
    except Exception as e:
        return False, {"error": str(e)}

@app.post('/set/cookie/{id}')
async def set_cookie(res: Response, id: int):
    id = int(id)
    age = 10 * 60 * 60 * 24
    value = uuid4().__str__()
    await saveCookie(value, id, age)
    res.set_cookie(
        key="auth_token",
        value=value,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
        max_age=age
    )

@app.get('/get/cookie/{id}')
async def get_cookie(req: Request, id: int):
    token = req.cookies.get("auth_token")
    if not token:
        return {"authenticated": False}
    valid, session = await getCookie(id, token)
    if valid is None:
        return {"authenticated": False, "error": "Session Expired!"}
    elif valid:
        return {"authenticated":True, "user": session}
    elif session.get("error",None):
        return {"authenticated":False, "error":session.get("error", "Cannot read Session data!")}
    else:
        return {"authenticated":False}