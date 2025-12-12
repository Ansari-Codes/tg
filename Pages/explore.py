from UI import Label, Input, Button, Icon, RawCol, RawRow, Card, SoftBtn, Choice, AddSpace, Header, Html, confirm, Dialog, navigate, Select, ui, Notify
from ENV import NAME, ICON
from models import Variable
from database.brows import getPaginated
from storage import getUserStorage, userID
from loading import showLoading

def proj(project: dict):
    slug = project.get('slug')
    with RawRow().classes("relative w-full grid grid-cols-6 gap-2", remove="flex flex-row"):
        Label(project.get("title", "Untitled").title()).classes("text-xl font-bold break-words break-all overflow-hidden col-span-5")
        Button(config=dict(icon="open_in_new"), on_click=lambda:navigate(f"/project/{slug}")).props("dense", remove="push").classes("px-1.5 h-fit")
    with RawRow().classes("w-full h-12"):
        Html(f'<canvas id="t-{slug}-canvas" class="w-full h-full" style="transform-origin: 0 0; background:white;"></canvas>')
        ui.run_javascript(project.get("jscode","").replace("{{canvas}}", f"t-{slug}-canvas", 1))
    with RawRow().classes("w-full px-2 gap-1 items-end"):
        with RawRow().classes("w-fit font-bold items-end"):
            if project.get("status"):
                Icon("public", 'xs', 'green-700').classes("dark:text-green-300")
                Label("Public").classes("text-md text-green-700 dark:text-green-300")
            else: 
                Icon("drafts", 'xs', 'yellow-600')
                Label("Draft").classes("text-md text-yellow-600 dark:text-yellow ")
        with RawRow().classes("w-fit font-bold items-end"):
            Icon("favorite", 'xs', 'red')
            Label(project.get("likes",0)).classes("text-md text-red")
        with RawRow().classes("font-bold items-end"):
            Icon("person", "xs", "primary")
            Label(project.get("owner_name", "Anonymous").title()).classes("text-priamry text-md")

def sectionLabel(text):
    return Label(text).classes("w-full text-md font-semibold")

async def render():
    __w = []
    page = Variable(1) # type: ignore
    per_page = Variable(50) # type: ignore
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
        with c:
            if projects.success:
                with RawCol().classes("w-full p-2 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-2"):
                    for project in projects.data:
                        with Card().classes("w-full p-4 gap-2 max-w-full break-words break-all overflow-hidden"):
                            proj(project)
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
                    if len(projects.data) < pg:  # type: ignore
                        next_btn.disable()
            else:
                Label("Unable to fetch projects!").classes("text-xl font-bold text-red-500")
        for _ in __w: _.set_enabled(True)
    d = Dialog()
    with ui.header().classes("flex items-center bg-secondary"):
        Label("Explore").classes("text-xl font-bold")
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
            Button(config=dict(icon="search"), on_click=lambda s=sq:search(s)).bind_enabled_from(sq, "value", backward=lambda x:x.strip()).props("unelevated", remove="push").classes("rounded-l-0")
        with RawRow().classes("w-fit h-fit gap-1 justify-center items-center"):
            Label("Per Page: ").classes("text-xl font-semibold")
            ppg = Select(value=per_page.value, options=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        async def pppg(p):
            per_page.value = int(p.value) if p.value and p.value > 10 else 10
            page.value = 1
            await updateProjects()
        ppg.on_value_change(pppg)
    c = RawCol().classes("w-full h-fit max-h-[78vh] mt-2 justify-center items-center")
    await updateProjects()
