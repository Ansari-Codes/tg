from UI import Label, Input, Button, Icon, RawCol, RawRow, Card, SoftBtn, AddSpace, Header, Dialog, navigate, ui
from ENV import NAME, ICON
from models import Variable
from database.project import createEmtpyProject, getAllProjects
from storage import getUserStorage, userID

async def _ask_new_project():
    v = Variable()
    n = ui.notification("Creating project!", position='top-right', spinner=True, timeout=100, close_button=True, color='secondary')
    p = await createEmtpyProject()
    n.dismiss()
    slug = p.data.get("slug")
    navigate(f"/create/{slug}",True)

async def projects():
    Button("New", _ask_new_project, {"icon":"plus"})
    projects = await getAllProjects(userID())
    for project in projects.data:
        with Card().classes("w-full p-4 gap-2"):
            slug = project.get('slug')
            Label(project.get("title", "Untitled")).classes("text-xl font-bold")
            Label(f"ID: {project.get('id')}").classes("text-sm opacity-70")
            Label(f"Slug: {project.get('slug')}").classes("text-sm opacity-70")
            Label("Description:").classes("text-md font-semibold mt-2")
            Label(project.get("description", "") or "No description").classes("text-sm")
            Label("Likes:").classes("text-md font-semibold mt-2")
            Label(str(project.get("likes", 0))).classes("text-sm")
            Label("Python Code:").classes("text-md font-semibold mt-2")
            Label(project.get("pycode", "")).classes("text-xs bg-gray-200 p-2 rounded w-full")
            Label("JavaScript Code:").classes("text-md font-semibold mt-2")
            Label(project.get("jscode", "")).classes("text-xs bg-gray-200 p-2 rounded w-full")
            with RawRow():
                Button("Edit", lambda s=slug:navigate(f"/create/{s}",True))
                Button("View", lambda s=slug:navigate(f"/project/{s}",True))
    print(projects.data)
