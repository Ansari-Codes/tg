from comps import compLayout
from database.session import getCurrentUser
from loading import showLoading
from ENV import NAME
from UI import ui

async def render(token):
    w = showLoading(NAME)
    await ui.context.client.connected()
    res = await getCurrentUser(token)
    auth = res.success
    w.delete()
    await compLayout.CompHeader(auth)
    await compLayout.CompFooter(auth)
