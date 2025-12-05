from UI import Label, Header, Input, Button, TextArea, SoftBtn, Col, Row, AddSpace, Html, ui
from database.project import loadProject
from storage import getTabStorage, updateTabStorage

async def render(s):
    project = await loadProject(s)
    client = ui.context.client
    await client.connected()
    print(project)
    if project.success:
        updateTabStorage(project.data)
        pycode = project.data.get("pycode","")
        jscode = project.data.get("jscode","")
        title = project.data.get("title","")
        desc = project.data.get("description","")
        slug = s
    else: return

    with Header():
        Label("Create").classes("text-lg font-bold")
        AddSpace()
        Button("Run")
        Input()
        Button("Save")
    
    with ui.splitter() as s:
        with s.before:
            with Col():
                with ui.splitter() as sp:
                    with sp.before: TextArea(pycode)
                    with sp.after: TextArea()
        with s.after: Html('<canvas width="500px" height="500px"></canvas>')
