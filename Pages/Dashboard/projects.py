from UI import Label, Input, Button, Icon, RawCol, RawRow, Card, Html, Choice, AddSpace, Header, confirm, Dialog, navigate, Select, ui, Notify
from ENV import NAME, ICON
from models import Variable
from database.project import createEmtpyProject, getAllProjects, deleteProject
from storage import getUserStorage, userID
from loading import showLoading

async def _ask_new_project():
    n = ui.notification("Creating project...", position='bottom-left', color='primary',
                    spinner=True, timeout=100, close_button=True)
    try:
        p = await createEmtpyProject()
        n.dismiss()
        if not p.success:
            raise Exception(p.errors.get("other", ""))
        slug = p.data.get("slug")
        navigate(f"/create/{slug}",True)
    except Exception as e:
        n.dismiss()
        Notify(str(e), type="negative")

async def _del_prject(id, d, updater):
    async def __del_proj():
        n = ui.notification("Deleting project...", position='bottom-left', color='red-200',
                    spinner=True, timeout=100, close_button=True)
        try:
            p = await deleteProject(id)
            n.dismiss()
            if not p.success:
                raise Exception(p.errors.get("other", ""))
            Notify("Project deleted!", type="success")
        except Exception as e:
            n.dismiss()
            Notify(str(e), type="negative")
        finally:
            d.close()
            await updater()
    d.clear()
    with d:
        with Card():
            Label("Do you really want to delete this project?").classes("text-md font-semibold")
            with RawRow():
                Button("Yes", config=dict(icon='check'), on_click=__del_proj)
                Button("No", config=dict(icon='close'), on_click=d.close)
    d.open()

def proj(project: dict, del_proj=lambda i:()):
    slug = project.get('slug')
    def context_menu():
        with ui.context_menu():
            ui.menu_item("Edit", lambda:(navigate(f"/create/{slug}",True) if slug else None)).classes("bg-primary font-bold text-md")
            ui.menu_item("View", lambda:(navigate(f"/project/{slug}",True) if slug else None)).classes("bg-primary font-bold text-md")
            ui.menu_item("Delete", lambda:del_proj(project.get('id'))).classes("bg-red-500 font-bold text-md")
    with Label(project.get("title", "Untitled").title()).classes("text-xl font-bold break-words break-all overflow-hidden"):
        context_menu()
    with RawRow().classes("w-full aspect-square border-[1px] border-[var(--q-secondary)] rounded-sm"):
        Html(f'<canvas id="t-{slug}-canvas" class="w-full h-full"></canvas>')
        ui.run_javascript(project.get("jscode","").replace("{{thumbnail}}", "true").replace("{{canvas}}", f"t-{slug}-canvas", 1))
        context_menu()
    with RawRow().classes("w-full px-2 gap-1 items-end"):
        with RawRow().classes("w-fit font-bold items-end"):
            if project.get("status"):
                Icon("public", 'xs', 'green-700').classes("dark:text-green-300")
                Label("Public").classes("text-md text-green-700 dark:text-green-300")
            else: 
                Icon("drafts", 'xs', 'yellow-600')
                Label("Draft").classes("text-md text-yellow-600 dark:text-yellow ")
        with RawRow().classes("w-fit font-bold items-end"):
            Icon("thumb_up", 'xs', 'blue')
            Label(project.get("likes",0)).classes("text-md text-blue-500 dark:text-blue-400")
        with RawRow().classes("w-fit font-bold items-end"):
            Icon("visibility", 'xs', 'red')
            Label(project.get("views",0)).classes("text-md text-red-500")

def sectionLabel(text):
    return Label(text).classes("w-full text-md font-semibold")

async def projects(area):
    __w = []
    page = Variable(1) # type: ignore
    per_page = Variable(50) # type: ignore
    dialog = Dialog()
    async def ask():
        new.disable()
        await _ask_new_project()
        await updateProjects()
        new.enable()
    async def del_proj(id):
        await _del_prject(id,dialog, updateProjects)
    async def updateProjects(filters: dict | None = None):
        c.clear()
        filters = filters or {}
        for _ in __w: _.set_enabled(False)
        with c: showLoading('Projects', True).classes("w-full h-full max-h-[78vh]")
        pg = per_page.value
        projects = await getAllProjects(
            userID(),
            **filters,
            per_page=pg, # type: ignore
            page=page.value, # type: ignore
        )
        c.clear()
        with c:
            if projects.success:
                with RawCol().classes("w-full h-full"):
                    with RawCol().classes("w-full h-fit max-h-[75vh] overflow-y-auto"):
                        with RawCol().classes("w-full p-2 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-2"):
                            for project in projects.data:
                                with Card().classes("w-full p-4 gap-2 max-w-full break-words break-all overflow-hidden"):
                                    proj(project, del_proj)
                    area.props("relative")
                    with RawRow().classes(
                        "absolute bottom-2 left-1/2 transform -translate-x-1/2 bg-primary gap-3 p-2 rounded-full shadow-xl items-center justify-center"
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
    with RawRow().classes("w-full gap-2"):
        with RawRow().classes("w-full sm:w-fit"):
            async def search(s):
                page.set(1)
                await updateProjects({"search_q":s.value.__str__()})
            sq = Input(on_change=search).classes(
                "transition-all duration-300 ease-in-out "
                "w-[80%] "
                "sm:w-[200px] ",
            ).props("input-class='rounded-r-0'")
            Button(config=dict(icon="search"), on_click=lambda s=sq:search(s)).props("unelevated", remove="push").classes("rounded-l-0 w-[18%]")
        new = Button(on_click=ask, config={"icon":"add"})
        ref = Button(on_click=updateProjects, config={"icon":"refresh"})
        AddSpace()
        with RawRow().classes("w-fit h-fit gap-1 justify-center items-center"):
            Label("Per Page: ").classes("text-xl font-semibold")
            ppg = Select(value=per_page.value, options=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        async def pppg(p):
            per_page.value = int(p.value) if p.value and p.value > 10 else 10
            page.value = 1
            await updateProjects()
        ppg.on_value_change(pppg)
        __w.append(ref)
        __w.append(new)
    c = RawCol().classes("w-full h-fit max-h-[78vh] mt-2 justify-center items-center")
    await updateProjects()
