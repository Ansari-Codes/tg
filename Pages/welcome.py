from comps import compLayout
from database.session import getCurrentUser
from loading import showLoading
from ENV import NAME
from UI import Button, ui, Link

async def render(token):
    def addButtons():
        auth = res.success and res.data
        if not auth:
            with d:
                Button("LogIn", link="/login")
                Button("SignUp", link="/signup")
            with m:
                Button("LogIn", link="/login")
                Button("SignUp", link="/signup")
        else:
            with d: Button("Dashboard", link="/dashboard")
            with m: Button("Dashboard", link="/dashboard")
        d.update()
        m.update()
        with f:
            if auth:
                Link("Dashboard", "/dashboard").classes("text-white")
            else:
                Link("LogIn", "/login").classes("text-white")
                Link("SignUp", "/signup").classes("text-white")
    w = showLoading(NAME)
    await ui.context.client.connected()
    w.delete()
    _,_, d, m = await compLayout.CompHeader()
    await compLayout.CompHero()
    f = await compLayout.CompFooter()
    res = await getCurrentUser(token)
    addButtons()