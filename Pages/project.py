from UI import Label, Button, RawCol, RawRow, Card, Input, Icon, Html, Logger, ui
from storage import getUserStorage, updateUserStorage
from database.project import loadProject
from loading import showLoading
from js import ZOOM_PAN

async def render(slug):
    c = showLoading(f"Project: {slug}")
    project = await loadProject(slug)
    data = project.data
    async def run():
        ui.run_javascript(data.get("jscode","").format(canvas="t-canvas"))
    uts = updateUserStorage
    gts = getUserStorage
    if project.success:
        Button("Run", run).classes("w-full")
        Button("Stop", lambda: ui.run_javascript("window.is_running = false;")).classes("w-full")
        c.delete()
        Html("""
        <div id="canvas-wrapper" 
            class="bg-gray-400 dark:bg-gray-800"
            style="width:100%; height:100%; overflow:hidden; position:relative;">
            <canvas id="t-canvas" width="1200" height="800"
                    style="transform-origin: 0 0; background:white;"></canvas>
        </div>
        """)
        ZOOM_PAN()
    else:
        Label("Error in loading the project!").classes("text-2xl text-red font-bold")

