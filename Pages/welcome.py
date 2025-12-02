from comps import compLayout
from storage import getUserStorage

async def render():
    auth = getUserStorage()
    compLayout.CompHeader()
    compLayout.CompFooter()
