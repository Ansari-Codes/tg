from UI import Label, Input, Button, Icon, RawCol, RawRow, Card, AddSpace, Header, Dialog, navigate, Notify, ui
from ENV import NAME, ICON
from models import Variable
from .Dashboard import *
from loading import showLoading

async def changePage(area:ui.element, var:Variable, name:str, triggerer=None, user_id=None,name_=None):
    area.clear()
    name = name.lower()
    with area:
        var.value = name.title()
        if triggerer:
            for t in triggerer:t.set_enabled(False)
        try:
            if name == 'dashboard': await dashbd(area,user_id,name_) #type:ignore
            elif name == 'projects': await projects(area,user_id) #type:ignore
            elif name == 'analytics': await analytics(area)
            elif name == 'settings': await settings(area)
        except Exception as e:
            Notify(f"We cannot take you to {name}!", type="negative")
        finally:
            if triggerer:
                for t in triggerer:t.set_enabled(True)
    ui.run_javascript(f"localStorage.setItem('tab', '{name}')")

def createDrawer(area,var,user_id,uname):
    with ui.drawer('left').classes("bg-primary") as drawer:
        Label(ICON + NAME).classes("text-2xl w-full text-center font-bold border-b-[1px]")
        btns = {
            "Dashboard": {
                "icon": "dashboard"
            },
            "Projects": {
                "icon": "code"
            },
        }
        with RawCol().classes("w-full h-full gap-1"):
            bs = []
            for name, kw in btns.items():
                b = Button(name, config=kw).classes("w-full bg-secondary").props('align="left"')
                bs.append((lambda b=b: b)())
                b.on_click(lambda _,name=name,b=bs: changePage(area, var, name, b,user_id,uname))
            ab = Button("Analytics", config=dict(icon="auto_graph")).classes("w-full bg-secondary").props('align="left"')
            bs.append(ab)
            ab.on_click(lambda bs=bs:changePage(area, var, "analytics",bs,user_id,uname))
            sb = Button("Settings", config=dict(icon="settings")).classes("w-full bg-secondary").props('align="left"')
            bs.append(sb)
            sb.on_click(lambda bs=bs:changePage(area, var, "settings",bs,user_id,uname))
            db = Button("Docs", config=dict(icon="book")).classes("w-full bg-secondary").props('align="left"')
            bs.append(db)
            db.props("href='/docs' target='_blank'")
        return drawer, bs

import asyncio

async def render(token, user_id, name):
    loading = showLoading("Dashboard").classes("w-full h-[73vh]")
    var = Variable()
    d = []
    def toggle(): 
        if d:d[0].toggle()
    context = ui.context
    await context.client.connected()
    await asyncio.sleep(1)
    with Header() as header:
        Icon('menu','md').on('click', toggle).classes(
                "rounded transition-all duration-200 "
                "hover:shadow-md hover:brightness-75 "
                "cursor-pointer"
            )
        AddSpace()
        Label(model=var, model_configs={"strict":False}).classes("text-2xl font-bold font-sans")
        AddSpace()
        Label("")
    header.classes("p-2 m-0")
    area = ui.element().classes("w-full")
    dbs = createDrawer(area, var,user_id,name)
    drawer = dbs[0]
    bs = dbs[-1]
    d.append(drawer)
    page_layout = context.client.layout
    page_layout.props(remove='view', add='view="lHh lpR lFf"')
    try:
        tab = await ui.run_javascript("localStorage.getItem('tab')")
        tab = tab if tab and tab.strip() else "dashboard"
    except Exception as e:
        tab = 'dashboard'
    loading.delete()
    await changePage(area, var, tab,bs,user_id,name)
