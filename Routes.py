from Pages.welcome import render as rw
from Pages.Auth.signup import render as rs
from ENV import ui

@ui.page("/")
async def cw():
    await rw()

@ui.page("/signup")
async def csp():
    await rs()
