from UI import Label, Button, RawCol, RawRow, ui, Html, Icon, AddSpace
from storage import getUserStorage, updateUserStorage
from database.project import loadProjectWithOwner
from loading import showLoading
from js import ZOOM_PAN
import ENV

async def render(slug):
    c = showLoading(f"Project: {slug}")
    context = ui.context.client
    await context.connected()

    project = await loadProjectWithOwner(slug)
    data = project.data

    async def run():
        ui.run_javascript(data.get("jscode", "").replace("{{canvas}}", "t-canvas", 1))

    async def stop():
        ui.run_javascript("window.is_running = false;")

    c.delete()
    with ui.header().classes("flex items-center"):
        Html(ENV.ICON + ENV.NAME).classes("text-xl font-bold")
        AddSpace()
        Button("Explore").props("href='/explore' target='_blank'")
        Button("Dashboard").props("href='/dashboard' target='_blank'")

    if project.success:
        with ui.element().classes("w-full h-full flex flex-col sm:grid sm:grid-cols-2 gap-2 px-1 lg:px-[10vw]"):

            # Left column: buttons + canvas
            with RawCol().classes(
                "w-full sm:w-full h-fit gap-2"
            ):
                # Buttons row
                with RawRow().classes("w-full gap-2 h-fit justify-start sm:justify-start items-center"):
                    Label(data.get("title", "Untitled").title()).classes("text-xl font-semibold")
                    AddSpace()
                    with Button(config=dict(icon="arrow_drop_down_circle")):
                        with ui.menu().props("auto-close"):
                            with RawCol().classes("w-fit gap-1 p-1"):
                                Button(on_click=run, config=dict(icon="play_circle", color="primary"))
                                Button(on_click=stop, config=dict(icon="stop", color="negative"))
                                Button(config=dict(icon="code", color="positive"))

                # Canvas row
                Html(f"""
                <div id="canvas-wrapper" 
                    class="w-full sm:w-full aspect-square sm:aspect-[1/1] overflow-hidden bg-gray-200 border rounded">
                    <canvas id="t-canvas" 
                            style="background:white; transform-origin:0 0; width:100%; height:100%;">
                    </canvas>
                </div>
                """).classes("w-full h-full flex justify-center items-center")

                # Enable zoom/pan
                ZOOM_PAN()

            # Right column: description
            with RawCol().classes(
                "w-full sm:w-full h-fit sm:h-full overflow-auto border-2 border-[var(--q-secondary)] rounded-md"
            ):
                with RawRow().classes("bg-secondary w-full p-1 text-xl text-left font-bold"):
                    Label("Description")
                ui.markdown(
                    data.get("description", "No Description provided!"),
                    extras=["fenced-code-blocks", "tables", "mermaid", "latex"]
                ).classes("m-3 max-h-[60%] h-full overflow-auto bg-primary")
                with ui.element().classes("w-full h-[30%] border-t-2 border-[var(--q-secondary)]"):
                    likes = data.get("likes", "N/A")
                    with RawRow().classes("w-fit h-fit items-center"):
                        Icon("favorite", "sm", "red")
                        Label(likes).classes("text-lg font-semibold text-red-500")
    else:
        Label("Error loading the project!").classes("text-2xl text-red font-bold")
