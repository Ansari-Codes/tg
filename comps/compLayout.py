from UI import Header, Label, Html, Button, AddSpace, Footer, Link, navigate, navBar, Card, Col, RawCol, RawRow, Row
from ENV import NAME, ICON

async def CompHeader(auth):
    with Header() as h:
        Html(ICON).classes("text-2xl h-full")
        Label(NAME).classes("font-bold text-2xl h-full")
        AddSpace()
        links = {}
        links['Explore'] = "/explore"
        links['Dashboard'] = {"link":"/dashboard", "cond":auth}
        links['SignUp'] = {"link":"/signup", "cond":not auth}
        links['LogIn'] = {"link":"/login", "cond":not auth}
        links['LogOut'] = {"link":"/clear-cookie", "cond":auth}
        navBar(links=links)
    return h

async def CompHero(auth):
    with Card().classes("w-full h-fit"):
        with RawRow().classes("w-fit h-fit gap-1 items-center"):
            Label(ICON).classes(" text-4xl lg:text-6xl ")
            Label(NAME).classes(" text-4xl lg:text-6xl font-semibold")

async def CompFooter(auth):
    with Footer() as f:
        if auth: 
            Link("Dashboard", link='/dashboard')
        else:
            Link("SignUp", link="/signup").classes("text-white hover:text-black")
            Link("LogIn", link='/login').classes("text-white hover:text-black")
    return f

