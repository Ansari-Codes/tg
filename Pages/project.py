from UI import Label, Button, RawCol, RawRow, ui, Html, Icon, AddSpace, Notify
from database.project import loadProjectWithOwner, likeAProject, viewAProject, hasLiked
from database.session import getCurrentUser
from loading import showLoading
from js import ZOOM_PAN
import ENV

async def render(slug, token):
    c = showLoading(f"Project: {slug}")
    context = ui.context.client
    await context.connected()

    project = await loadProjectWithOwner(slug)
    user = await getCurrentUser(token)
    data = project.data
    print(project)
    def userID():
        return user.data.get("id")

    async def run():
        ui.run_javascript(data.get("jscode", "").replace("{{thumbnail}}", "false", 1).replace("{{canvas}}", "t-canvas", 1))

    async def stop():
        ui.run_javascript("window.is_running = false;")

    async def likeProject():
        if not like_button:return
        if not userID(): 
            Notify("LogIn first to like!")
            return
        like_button.set_enabled(False)
        try:
            likes = await likeAProject(data.get("id", None), userID())
            d = likes.data
            if likes.success:
                like_label.set_text(d.get("likes", "N/A"))
                data['likes'] = d.get("likes", 0)
                Notify(d.get("action", "").title())
                if d.get("action", "") == "liked":
                    like_button.set_icon(icon="thumb_down")
                    like_button.props("color='red'")
                else:
                    like_button.set_icon("thumb_up")
                    like_button.props("color='primary'")
            else:
                Notify("An Error occured while liking!", type="negative")
        finally:
            like_button.set_enabled(True)

    if project.success:
        _ = await viewAProject(data.get("id", None), userID())
        print(_)
        if _.success and not (_.meta.get("view", "") == "already viewed"):
            data['views'] = _.data.get("views", 0)
        elif (_.meta.get("view", "") == "already viewed"):
            pass
        else:
            Notify(_.errors.get("view", "An error occured in viewing!"), type="negative")
        hasliked = await hasLiked(data.get("id", None), userID())
        like_button = Button(
            on_click=likeProject, #type:ignore
            config=dict(icon="thumb_up", color="blue"),
        ).classes("w-fit mt-2")
        if hasliked.success:
            if bool(hasliked.data):
                    like_button.set_icon(icon="thumb_down")
                    like_button.props("color='red'")
            else:
                like_button.set_icon("thumb_up")
    else:
        like_button = None
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
                "w-full h-fit gap-2"
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
                with RawRow().classes(
                    "w-full border-2 border-[var(--q-secondary)] rounded-md p-3 gap-2 bg-gray-50 flex-grow "
                ) as lll:
                    with ui.element().classes("h-full flex flex-grow border-r-2 border-[var(--q-primary)]"):
                        with RawCol():
                            Label(data.get('owner_name', 'Unknown').title()).classes("text-xl font-semibold")
                            Label(data.get('owner_email', 'N/A')).classes("text-sm")
                        with RawRow().classes("gap-4 text-sm"):
                            with RawRow().classes("text-blue-500 dark:text-blue-400"):
                                Icon("thumb_up")
                                like_label = Label(data.get('likes', 0)).classes("text-xl")
                            with RawRow().classes("text-yellow-800 dark:text-yellow-400"):
                                Icon("visibility",)
                                Label(data.get('views', 0)).classes("text-xl")
                    if like_button:like_button.move(lll)

            # Right column: description/Info
            with RawCol().classes("w-full h-fit gap-2"):
                with RawCol().classes(
                    "w-full overflow-auto border-2 border-[var(--q-secondary)] rounded-md"
                ):
                    with RawRow().classes(
                        "bg-secondary w-full p-2 text-lg font-bold"
                    ):
                        Label("Description")
                    ui.markdown(
                        data.get("description", "No Description provided!"),
                        extras=["fenced-code-blocks", "tables", "mermaid", "latex"]
                    ).classes("p-2 overflow-auto")
    else:
        Label("Error loading the project!").classes("text-2xl text-red font-bold")
