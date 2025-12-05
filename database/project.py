from db import RUN_SQL, PROJECTS
from models import Response
from .helpers import isUnique, escapeSQL, randomstr, rnd
from storage import getUserStorage

async def unique(item, col):
    return await isUnique(item, col, PROJECTS)

async def createProject(
    name: str
):
    name = escapeSQL(name.lower())
    res = Response()
    if not await unique(name, 'title'):res.errors['title']="Title already exists"
    if not res.success:return res
    slug=getUserStorage().get("name",randomstr())+randomstr()+rnd()+getUserStorage().get("id",rnd())
    
