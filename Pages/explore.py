from UI import Label, Input, Button, Icon, RawCol, RawRow, Card, Choice, AddSpace, Header, Html, confirm, Dialog, navigate, Select, ui, Notify
from ENV import NAME, ICON
from models import Variable
from database.brows import getPaginated
from loading import showLoading

def proj(project: dict, js=None):
    slug = project.get('slug')
    with RawRow().classes("relative w-full grid grid-cols-6 gap-2", remove="flex flex-row"):
        Label(project.get("title", "Untitled").title()).classes("text-xl font-bold break-words break-all overflow-hidden col-span-5")
        Button(config=dict(icon="open_in_new"), link=f"/project/{slug}", new_tab=True).props("dense", remove="push").classes("px-1.5 h-fit")
    with RawRow().classes("w-full aspect-square border-[1px] border-[var(--q-secondary)] rounded-sm"):
        Html(f'<canvas id="t-{slug}-canvas" class="w-full h-full"></canvas>')
        js.append(project.get("jscode","").replace("{{thumbnail}}", "true", 1).replace("{{canvas}}", f"t-{slug}-canvas", 1)) #type:ignore
    with RawRow().classes("w-full px-2 gap-1 items-center"):
        with RawRow().classes("w-fit font-bold items-center"):
            Icon("visibility", 'xs', 'yellow-600')
            Label(project.get("views", 0)).classes("text-md text-yellow-600 dark:text-yellow ")
        with RawRow().classes("w-fit font-bold items-center"):
            Icon("thumb_up", 'xs', 'blue')
            Label(project.get("likes",0)).classes("text-md text-blue-500")
        with RawRow().classes("font-bold items-center"):
            Icon("person", "xs", "primary")
            Label(project.get("owner_name", "Anonymous").title()).classes("text-primary text-md")

def sectionLabel(text):
    return Label(text).classes("w-full text-md font-semibold")

async def render():
    await ui.context.client.connected()
    __w = []
    page = Variable(1) # type: ignore
    per_page = Variable(10) # type: ignore
    js = []
    async def updateProjects(filters: dict | None = None):
        c.clear()
        filters = filters or {}
        for _ in __w: _.set_enabled(False)
        with c: showLoading('Projects', True).classes("w-full h-full max-h-[78vh]")
        pg = per_page.value
        projects = await getPaginated(
            **filters,
            per_page=pg, # type: ignore
            page=page.value, # type: ignore
        )
        c.clear()
        js.clear()
        with c:
            if not projects.success:
                Label("Unable to fetch projects!").classes("text-xl font-bold text-red-500")
                print("Error Fetching projects: explorer.py: ", projects.errors)
            else:
                projects_list = projects.data or []
                if not isinstance(projects_list, (list, tuple)):
                    # defensive fallback
                    Label("Unable to fetch projects!").classes("text-xl font-bold text-red-500")
                elif len(projects_list) == 0:
                    Label("No projects found.").classes("text-xl font-semibold")
                else:
                    with RawCol().classes("w-full p-2 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-2"):
                        for project in projects_list:
                            with Card().classes("w-full p-4 gap-2 max-w-full break-words break-all overflow-hidden"):
                                proj(project, js)

                # pagination controls (always rendered regardless of whether we had items,
                # but disabled appropriately)
                with RawRow().classes(
                    "fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-primary gap-3 p-2 rounded-full shadow-xl items-center justify-center"
                ):
                    async def prev():
                        page.set(max(1, page.value - 1))  # type: ignore
                        await updateProjects(filters)
                    prev_btn = Button("◀", on_click=prev).props("rounded")
                    if page.value <= 1:  # type: ignore
                        prev_btn.disable()
                    Label(f"Page {page.value}").classes("text-sm font-semibold text-white w-fit")
                    async def nex():
                        page.set(page.value + 1)  # type: ignore
                        await updateProjects(filters)
                    next_btn = Button("▶", on_click=nex).props("rounded")
                    # use projects_list here (defensive)
                    try:
                        if isinstance(projects_list, (list, tuple)) and len(projects_list) < pg:  # type: ignore
                            next_btn.disable()
                    except Exception:
                        next_btn.disable()
        for _ in __w: _.set_enabled(True)
        for i in js:ui.run_javascript(i)
    d = Dialog()
    with ui.header().classes("flex items-center bg-secondary"):
        Label("Explore").classes("text-2xl font-bold")
        AddSpace()
        with RawRow().classes("w-fit"):
            async def search(s):
                page.set(1)
                await updateProjects({"search_q":s.value.__str__()})
            sq = Input().classes(
                "transition-all duration-300 ease-in-out "
                "w-[200px] "
                "hover:w-[250px] ",
            ).props("input-class='rounded-r-0'")
            Button(config=dict(icon="search"), on_click=lambda s=sq:search(s)).props("unelevated", remove="push").classes("rounded-l-0")
        with RawRow().classes("w-fit h-fit gap-1 justify-center items-center"):
            Label("Per Page: ").classes("text-xl font-semibold")
            ppg = Select(value=per_page.value, options=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        async def pppg(p):
            per_page.value = int(p.value) if p.value and p.value > 10 else 10
            page.value = 1
            await updateProjects()
        ppg.on_value_change(pppg)
    c = RawCol().classes("w-full mt-2 justify-center items-center")
    await updateProjects()
