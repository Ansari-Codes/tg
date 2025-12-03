from Pages.welcome import render as rw
from Pages.Auth.signup import render as rs
from Pages.dashboard import render as rd
from ENV import ui

@ui.page("/")
async def cw():
    await rw()

@ui.page("/signup")
async def csp():
    await rs()

@ui.page("/dashboard")
async def cd():
    await rd()
