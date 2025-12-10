from UI import Label, Input, Card, Col, Row, RawCol, RawRow, TextArea, SoftBtn, Link, Button, Html, Icon, Notify, ui, AddSpace, navigate
from database.dashb import getUser, countProjects, getLatestProjects, getAllProjectsWithoutPaginationOrSearch
from storage import getUserStorage, userID
from loading import showLoading
from plotly.graph_objects import Figure, Scatter

async def dashbd(area):
    area.clear()
    loading = showLoading("Dashboard", True).classes("w-full h-full")
    user = getUserStorage()
    pr = (await countProjects(userID()))
    p = pr.data
    projects = p.get("projs","N/A") or "0"
    drafts = p.get("draft", "N/A") or "0"
    pubs = p.get("pubs", "N/A") or "0"
    likes = p.get("likes", "N/A") or "0"
    latest = await getLatestProjects(userID())
    errors = {**pr.errors, **latest.errors}
    projectss = await getAllProjectsWithoutPaginationOrSearch(userID())
    if errors:
        for name, e in errors.items():
            Notify(e, type='negative')
    try:
        Html(f"Hi, <span class='text-primary'>{user.get('name', '').title()}!</span>").classes("w-full text-5xl font-bold mb-2")
        with RawRow().classes("w-full p-2 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-4 xl:grid-cols-4 2xl:grid-cols-5 gap-2", remove='flex flex-row'):
            with Card().classes("h-fit"):
                with RawCol().classes("w-full gap-1"):
                    Label(f"Total Likes").classes("text-lg font-bold")
                    with RawRow().classes("w-full gap-1 text-red-500 items-center"):
                        Icon("favorite", "lg");AddSpace()
                        Label(likes).classes("text-4xl font-extrabold")
            with Card().classes("h-fit"): 
                with RawCol().classes("w-full gap-1"):
                    Label(f"Total Projects").classes("text-lg font-bold")
                    with RawRow().classes("w-full gap-1 text-secondary items-center"):
                        Icon("code", "lg");AddSpace()
                        Label(projects).classes("text-4xl font-extrabold")
            with Card().classes("h-fit"): 
                with RawCol().classes("w-full gap-1"):
                    Label(f"Draft Projects").classes("text-lg font-bold")
                    with RawRow().classes("w-full gap-1 text-yellow-700 dark:text-yellow-500 items-center"):
                        Icon("drafts", "lg");AddSpace()
                        Label(drafts).classes("text-4xl font-extrabold")
            with Card().classes("h-fit"): 
                with RawCol().classes("w-full gap-1"):
                    Label(f"Public Projects").classes("text-lg font-bold")
                    with RawRow().classes("w-full gap-1 text-green-500 items-center"):
                        Icon("public", "lg");AddSpace()
                        Label(pubs).classes("text-4xl font-extrabold")
        if latest.data:
            with RawRow().classes("w-full h-full justify-between"):
                with RawCol().classes("w-full sm:w-full md:w-[30%] gap-2 p-1"):
                    Label("Some latest projects...").classes("text-lg font-semibold italic")
                    for project in latest.data:
                        with Card():
                            with RawRow().classes("w-full gap-1"):
                                Label(project.get("title","").title()).classes("text-lg font-semibold max-w-[50%] truncate")
                                AddSpace()
                                Icon("drafts" if not project.get("status") else "public", 'sm'
                                    ).classes("p-1").classes("text-yellow-700 dark:text-yellow-500" if not project.get("status") else "text-green-500")
                                Icon("edit", 'sm'
                                    ).classes("p-1 bg-primary rounded-sm cursor-pointer text-sm"
                                    ).on('click', lambda _,s=project.get("slug"):(navigate(f"/create/{s}",True) if s else None))
                                Icon("open_in_new", 'sm'
                                    ).classes("p-1 bg-primary rounded-sm cursor-pointer text-sm"
                                    ).on('click', lambda _,s=project.get("slug"):(navigate(f"/project/{s}",True) if s else None))
                with RawCol().classes("w-full md:max-w-[60%] md:w-[60%] p-1"):
                    fig = Figure(Scatter(x=[p.get("title", "") for p in projectss.data], y=[p.get("likes", "") for p in projectss.data]))
                    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
                    fig_dict = fig.to_dict()
                    fig_dict['config'] = {"displaylogo":False}
                    ui.plotly(fig_dict).classes("w-full h-full")
    except Exception as e:
        Label(f"Error Occured!").classes("text-2xl text-red p-2")
    loading.delete()
