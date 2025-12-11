from Pages.welcome import render as rw
from Pages.Auth.signup import render as rs
from Pages.Auth.login import render as rl
from Pages.dashboard import render as rd
from Pages.create import render as rc
from Pages.explore import render as re
from Pages.project import render as rp
from storage import getUserStorage
from UI import navigate, INIT_THEME
from ENV import ui

def auth(): return getUserStorage().get("auth",False)

@ui.page("/")
async def cw(): 
    INIT_THEME()
    await rw()

@ui.page("/explore")
async def cb(): 
    INIT_THEME()
    await re()

@ui.page("/project/{slug}")
async def cp(slug: str): 
    INIT_THEME()
    await rp(slug)

@ui.page("/signup")
async def csp(redirectTo: str = '/dashboard'):
    print("SignUp: ", getUserStorage()) 
    INIT_THEME()
    if not auth(): await rs(redirectTo)
    else: navigate(redirectTo)

@ui.page("/login")
async def csl(redirectTo: str = '/dashboard'):
    print("Login: ", getUserStorage()) 
    INIT_THEME()
    if not auth(): await rl(redirectTo)
    else: navigate(redirectTo)

@ui.page("/dashboard")
async def cd():
    print("Dashboard: ", getUserStorage()) 
    INIT_THEME()
    if auth(): await rd() # type: ignore
    else: navigate(f"/login?redirectTo=/dashboard")

@ui.page("/create/{slug}")
async def cc(slug: str):
    print("Creator: ", getUserStorage()) 
    INIT_THEME()
    if auth(): await rc(slug)
    else: navigate(f"/login?redirectTo=/create/{slug}")

