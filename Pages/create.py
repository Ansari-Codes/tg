from UI import Label, Header, Input, Button, TextArea, SoftBtn, Col, Row, AddSpace, Html, ui
from database.project import loadProject
from storage import updateTabStorage

async def render(slug):
    project = await loadProject(slug)
    context = ui.context.client
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
                    with sp.before:
                        TextArea()
                    with sp.after:
                        TextArea()
        with s.after:
            Html('<canvas width="500px" height="500px" ></canvas>')

