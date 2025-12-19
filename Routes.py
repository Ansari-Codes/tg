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

@ui.page("/")
async def cw(request: Request): 
    INIT_THEME()
    token = request.cookies.get("auth_token")
    print("Auth token Dashboard:", token)
    await rw(token)

@ui.page("/explore")
async def cb(): 
    INIT_THEME()
    await re()

@ui.page("/project/{slug}")
async def cp(slug: str, request: Request): 
    INIT_THEME()
    token = request.cookies.get("auth_token")
    print("Auth token Project viewer:", token)
    await rp(slug, token)

@ui.page("/signup")
async def css(redirectTo: str = '/dashboard', request: Request = None, res: Response = None): #type:ignore
    INIT_THEME()
    if request:
        token = request.cookies.get("auth_token")
        print("Auth token SignUp:", token)
    else:
        token = None
    if not token : await rs(redirectTo,response=res)
    else: navigate(redirectTo)

@ui.page("/login")
async def csl(redirectTo: str = '/dashboard', request: Request = None, res: Response = None): #type:ignore
    INIT_THEME()
    if request:
        token = request.cookies.get("auth_token")
        print("Auth token LogIn:", token)
    else:
        token = None
    if not token : await rl(redirectTo,response=res)
    else: navigate(redirectTo)

@ui.page("/set-cookie/{id}")
async def set_cookie(id: int, redirectTo: str = '/dashboard'):
    res = RedirectResponse(redirectTo)
    id = int(id)
    age = 15 * 60 * 60 * 24
    value = uuid4().__str__()
    c = showLoading("")
    try:
        await saveCookie(value, id, age)
    except Exception as e:
        return HTMLResponse(f"<span style='color: red;font-size:100px;'>An error occured!</span><br><span style='color: gray;font-size:15px;'>{e}</span>")
    res.set_cookie(
        key="auth_token",
        value=value,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
        max_age=age
    )
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
    return res

@ui.page("/dashboard")
async def cd(request: Request):
    INIT_THEME()
    token = request.cookies.get("auth_token")
    print("Auth token Dashboard:", token)
    if token: await rd(token) #type:ignore
    else: navigate("/login?redirectTo=/dashboard")

@ui.page("/create/{slug}")
async def cc(slug: str, request: Request):
    INIT_THEME()
    token = request.cookies.get("auth_token")
    print("Auth token Editor:", token)
    if token: await rc(slug,token) #type:ignore
    else: navigate(f"/login?redirectTo=/create/{slug}")

# @ui.page("/create")
# async def ccc():
#     await rc(slug=None)