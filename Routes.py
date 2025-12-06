from Pages.welcome import render as rw
from Pages.Auth.signup import render as rs
from Pages.Auth.login import render as rl
from Pages.dashboard import render as rd
from Pages.create import render as rc
from storage import getUserStorage
from UI import navigate
from ENV import ui

def auth(): return getUserStorage().get("auth",False)

@ui.page("/")
async def cw(): await rw()

@ui.page("/signup")
async def csp(redirectTo: str = '/dashboard'):
    if not auth(): await rs(redirectTo)
    else: navigate(redirectTo)

@ui.page("/login")
async def csl(redirectTo: str = '/dashboard'):
    if not auth(): await rl(redirectTo)
    else: navigate(redirectTo)

@ui.page("/dashboard")
async def cd():
    if auth(): await rd()
    else: navigate(f"/login?redirectTo=/dashboard")

@ui.page("/create/{slug}")
async def cc(slug: str):
    if auth(): await rc(slug)
    else: navigate(f"/login?redirectTo=/create/{slug}")
