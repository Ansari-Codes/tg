from Pages.welcome import render as rw
from Pages.Auth.signup import render as rs
from Pages.Auth.login import render as rl
from Pages.dashboard import render as rd
from Pages.create import render as rc
from ENV import ui

@ui.page("/")
async def cw():
    await rw()

@ui.page("/signup")
async def csp():
    await rs()

@ui.page("/login")
async def csl():
    await rl()

@ui.page("/dashboard")
async def cd():
    await rd()

@ui.page("/create/{name}")
async def cc(name: str):
    await rc(name)
