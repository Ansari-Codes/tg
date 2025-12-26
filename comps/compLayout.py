from UI import Header, Label, Html, Button, AddSpace, Footer, Link, navigate, navBar, Card, Col, RawCol, RawRow, Row
from ENV import NAME, ICON

async def CompHeader():
    with Header() as h:
        Html(ICON).classes("text-2xl h-full")
        Label(NAME).classes("font-bold text-2xl h-full")
        AddSpace()
        links = {}
        links['Explore'] = "/explore"
        links['Docs'] = "/docs"
        n,d,m = navBar(links=links)
    return h,n,d,m

async def CompHero():
    with Card().classes("w-full h-fit"):
        with RawRow().classes("w-fit h-fit gap-1 items-center"):
            Label(ICON).classes(" text-4xl lg:text-6xl ")
            Label(NAME).classes(" text-4xl lg:text-6xl font-semibold")

async def CompFooter():
    return Footer()

