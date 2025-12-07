from UI import Label, Input, Button, Icon, RawCol, RawRow, Card, SoftBtn, AddSpace, Header, Dialog, navigate, ui
from ENV import NAME, ICON
from models import Variable
from database.project import createEmtpyProject, getAllProjects
from storage import getUserStorage, userID

async def _ask_new_project():
    v = Variable()
    n = ui.notification("Creating project!", position='top-right', spinner=True, timeout=100, close_button=True, color='secondary')
    p = await createEmtpyProject()
    n.dismiss()
    slug = p.data.get("slug")
    navigate(f"/create/{slug}",True)

def proj(project: dict):
    slug = project.get('slug')
    Label(project.get("title", "Untitled")).classes("text-xl font-bold")
    with RawRow().classes("w-full px-2 gap-1 items-center"):
        with RawRow().classes("w-fit font-bold items-center"):
            if project.get("status"): 
                Icon("public", 'sm')
                Label("Public").classes("text-lg")
            else: 
                Icon("drafts", 'sm')
                Label("Draft").classes("text-lg")
        with RawRow().classes("w-fit font-bold items-center"):
            Icon("favorite", 'sm')
            Label(project.get("likes",0)).classes("text-lg")
        AddSpace()
        Icon("edit", 'sm').classes("p-1 bg-primary rounded-sm cursor-pointer text-sm").on('click', lambda:navigate(f"/create/{slug}",True))
        Icon("open_in_new", 'sm').classes("p-1 bg-primary rounded-sm cursor-pointer text-sm").on('click', lambda:navigate(f"/project/{slug}",True))

async def projects():
    async def ask():
        btn.disable()
        await _ask_new_project()
        btn.enable()
    btn = Button("New", ask, {"icon":"add"})
    projects = await getAllProjects(userID())
    for project in projects.data:
        with Card().classes("w-full p-4 gap-2"): proj(project)
    print(projects.data)
