from UI import Label, Header, Input, Button, TextArea, SoftBtn, Col, Row, AddSpace, Html, Logger, ui
from database.project import loadProject
from storage import updateTabStorage as uts, getTabStorage as gts

async def render(slug):
    project = await loadProject(slug)
    project = project.data
    context = ui.context.client
    await context.connected()
    uts(project)
    with Header():
        Label("Create").classes("text-lg font-bold")
        AddSpace()
        Button("Run")
        Input()
        Button("Save")
    
    with ui.splitter().classes("w-full h-[84vh] p-0 m-0") as s:
        with s.before:
            with ui.splitter(horizontal=True).classes("w-full h-full") as sp:
                with sp.before:TextArea(
                    project.get("pycode", ""), 
                    autogrow=True,
                    inp_cls="border-0 hover:border-0"
                ).classes("w-full h-full pr-2 border-0 hover:border-0")
                with sp.after:Logger()
        with s.after:
            Html('<canvas class="w-full h-full bg-gray-50" ></canvas>').classes("w-full h-full")

