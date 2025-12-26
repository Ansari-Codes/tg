from Pages.welcome import render as rw
from Pages.Auth.signup import render as rs
from Pages.Auth.login import render as rl
from Pages.dashboard import render as rd
from Pages.create import render as rc
from Pages.explore import render as re
from Pages.project import render as rp
from UI import navigate, INIT_THEME
from ENV import ui
from fastapi import Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from app_endpoints import RUN_SQL, saveCookie, uuid4, deleteCookie
from loading import showLoading
from database.dashb import getUserName
from Documentation.docs import create_docs

@ui.page("/")
async def cw(request: Request): 
    INIT_THEME()
    token = request.cookies.get("auth_token")
    await rw(token)

@ui.page("/explore")
async def cb(): 
    INIT_THEME()
    await re()

@ui.page("/project/{slug}")
async def cp(slug: str, request: Request): 
    INIT_THEME()
    token = request.cookies.get("auth_token")
    id = request.cookies.get("user_id")
    await rp(slug, token, id) #type:ignore

@ui.page("/signup")
async def css(redirectTo: str = '/dashboard', request: Request = None, res: Response = None): #type:ignore
    INIT_THEME()
    if request:
        token = request.cookies.get("auth_token")
    else:
        token = None
    if not token : await rs(redirectTo,response=res) #type:ignore
    else: navigate(redirectTo)

@ui.page("/login")
async def csl(redirectTo: str = '/dashboard', request: Request = None, res: Response = None): #type:ignore
    INIT_THEME()
    if request:
        token = request.cookies.get("auth_token")
    else:
        token = None
    if not token : await rl(redirectTo,response=res) #type:ignore
    else: navigate(redirectTo)
AGE = 15 * 60 * 60 * 24
def addCookie(res, key, value):
    res.set_cookie(
        key=key,
        value=value,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
        max_age=AGE
    )

@ui.page("/set-cookie/{id}")
async def set_cookie(id: int, redirectTo: str = '/dashboard'):
    res = RedirectResponse(redirectTo)
    id = int(id)
    value = uuid4().__str__()
    c = showLoading("")
    try:
        await saveCookie(value, id, AGE)
        uesrname = await getUserName(id)
        if uesrname.success:
            name = uesrname.data.get("name")
        else:
            raise Exception("Cannot fetch username...")
    except Exception as e:
        return HTMLResponse(f"<span style='color: red;font-size:100px;'>An error occured!</span><br><span style='color: gray;font-size:15px;'>{e}</span>")
    addCookie(res, "auth_token", value)
    addCookie(res, "user_id", str(id))
    addCookie(res, "user_name", str(name))
    return res

@ui.page("/clear-cookie")
async def del_cookie(request:Request):
    res = RedirectResponse('/')
    value = request.cookies.get("auth_token")
    if value is None: return res
    c = showLoading("")
    try:
        await deleteCookie(value)
    except Exception as e:
        return HTMLResponse(f"<span style='color: red;font-size:100px;'>An error occured!</span><br><span style='color: gray;font-size:15px;'>{e}</span>")
    res.delete_cookie("auth_token")
    res.delete_cookie("user_id")
    res.delete_cookie("user_name")
    return res

@ui.page("/dashboard")
async def cd(request: Request):
    INIT_THEME()
    token = request.cookies.get("auth_token")
    id = request.cookies.get("user_id")
    name = request.cookies.get("user_name")
    if token: await rd(token, id, name) #type:ignore
    else: navigate("/login?redirectTo=/dashboard")

@ui.page("/create/{slug}")
async def cc(slug: str, request: Request):
    INIT_THEME()
    token = request.cookies.get("auth_token")
    if token: await rc(slug,token) #type:ignore
    else: navigate(f"/login?redirectTo=/create/{slug}")

@ui.page("/docs")
async def cdc():
    INIT_THEME()
    await create_docs()

# @ui.page("/create")
# async def ccc():
#     await rc(slug=None)