from UI import Button, Label, Html, Link, Header, ui, AddSpace

sections = {
    "Introduction": ("mds/intro.md", "intro"),
    "Dashboard": ("mds/dashboard.md", "dashboard"),
    "Editor": ("mds/create.md", "editor"),
    "TurtleAPI": ("mds/turtle.md", "turtle"),
    "GitHUB": ("Github", "github")
}

async def create_header():
    with ui.header():
        Label("TurtleGraphics/Docs")
        AddSpace()
        Button("Home", link="/")
        Button("Explore", link="/explore")

async def create_drawer():
    pass

async def create_docs():
    await create_header()

