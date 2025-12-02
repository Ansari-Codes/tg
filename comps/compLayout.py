from UI import Header, Label, Html, SoftBtn, AddSpace, Footer, Link
from storage import getUserStorage
from ENV import NAME, ICON

def CompHeader():
    auth = getUserStorage().get("auth", False)
    with Header() as h:
        Html(ICON).classes("text-2xl h-full")
        Label(NAME).classes("font-bold text-2xl h-full")
        AddSpace()
        if auth: SoftBtn("Dashboard", link='/dashboard')
        else:
            SoftBtn("SignUp", link="/signup")
            SoftBtn("LogIn", link='/login')
    return h

def CompFooter():
    auth = getUserStorage().get("auth", False)
    with Footer() as f:
        if auth: Link("Dashboard", link='/dashboard')
        else:
            Link("SignUp", link="/signup").classes("text-white hover:text-black")
            Link("LogIn", link='/login').classes("text-white hover:text-black")
    return f

