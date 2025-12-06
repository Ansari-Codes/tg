from UI import Label, Input, Button, Icon, RawCol, RawRow, Card, SoftBtn, AddSpace, Header, Dialog, navigate, ui
from ENV import NAME, ICON
from models import Variable
from database.project import createProject

def dashboard():
    pass

def _ask_new_project(d):
    d.clear()
    v = Variable()
    async def _c():
        p = await createProject(str(t.value))
        slug = p.data.get("slug")
        d.close()
        navigate(f"/create/{slug}",True)
    with d.classes("flex flex-col min-w-[300px] min-h-[5vh]"):
        with Card():
            t = Input(v, bindings={"strict":False}).classes("w-full")
            with RawRow():
                Button("Create",on_click=_c)
                Button("Cancel",on_click=d.close).props("color=red")
    d.open()

async def projects():
    dialog = Dialog()
    Button("New", lambda d=dialog:_ask_new_project(d), {"icon":"plus"})

def analytics():
    pass

def settings():
    pass

async def changePage(area:ui.element, var:Variable, name:str):
    area.clear()
    name = name.lower()
    with area:
        var.value = name.title()
        if name == 'dashboard': dashboard()
        elif name == 'projects': await projects()
        elif name == 'analytics': analytics()
        elif name == 'settings': settings()

def createDrawer(area,var):
    with ui.drawer('left').classes("bg-primary") as drawer:
        Label(ICON + NAME).classes("text-2xl w-full text-center font-bold border-b-[1px]")
        btns = {
            "Dashboard": {
                "icon": "dashboard"
            },
            "Projects": {
                "icon": "code"
            },
            "Analytics": {
                "icon": "bar_chart"
            },
        }
        with RawCol().classes("w-full h-fit gap-1"):
            for name, kw in btns.items():
                Button(name, on_click=lambda name=name: changePage(area, var, name), config=kw).classes("w-full bg-secondary").props('align="left"')
            Button("Settings", on_click=lambda:changePage(area, var, "settings"), config=dict(icon="settings")).classes("w-full bg-secondary").props('align="left"')
        return drawer

async def render():
    var = Variable()
    d = []
    def toggle(): 
        if d:d[0].toggle()
    context = ui.context
    with Header() as header:
        Button(config={
            "icon": "menu"
        }, on_click=toggle).classes("px-1 py-1 text-md")
        AddSpace()
        Label(model=var, model_configs={"strict":False}).classes("text-2xl font-bold font-sans")
        AddSpace()
        Label("")
    area = ui.element()
    d.append(createDrawer(area, var))
    await changePage(area, var, "dashboard")
    page_layout = context.client.layout
    page_layout.props(remove='view', add='view="lHh lpR lFf"')
