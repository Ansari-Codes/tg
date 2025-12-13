from UI import Header, Label, Html, Button, AddSpace, Footer, Link, navigate
from storage import getUserStorage, updateUserStorage
from ENV import NAME, ICON

async def CompHeader():
    auth = getUserStorage().get("auth", False)
    with Header() as h:
        Html(ICON).classes("text-2xl h-full")
        Label(NAME).classes("font-bold text-2xl h-full")
        AddSpace()
        Button("Explore", link='/explore')
        if auth:
            Button("Dashboard", link='/dashboard')
            Button("LogOut", on_click=lambda:[
                updateUserStorage({}, clear=True),
                navigate('/')
            ])
        else:
            Button("SignUp", link="/signup")
            Button("LogIn", link='/login')
    return h

async def CompFooter():
    auth = getUserStorage().get("auth", False)
    with Footer() as f:
        if auth: 
            Link("Dashboard", link='/dashboard').classes("text-white hover:text-black")
        else:
            Link("SignUp", link="/signup").classes("text-white hover:text-black")
            Link("LogIn", link='/login').classes("text-white hover:text-black")
    return f

