# ui file (snippet)
from UI import Card, Center, Input, Label, Row, Col, RawCol, RawRow, AddSpace, CheckBox, Notify, Button, navigate, Password
from models import Variable
from database.auth import signup, login

def validate(iv, ie, pv, pe):
    if not iv.value.strip().lower():
        ie.value = "Identifier is required!"
    if not pv.value.strip():
        pe.value = "Password is required!"
    if pe.value or ie.value:
        return False
    return True

async def lgn(iv, pv, ie, pe, l):
    if not validate(iv, ie, pv, pe):return
    iden = iv.value.strip().lower()
    pswd = pv.value.strip()
    res = await login(iden, pswd)
    if not res.success:
        Notify(res.errors.get("acc", "Unknown error occured!"), type='negative')
        return
    res.data['auth'] = True
    print("LogIn:", res.data) 
    id = int(res.data.get("id",0))
    navigate(f"/set-cookie/{id}?redirectTo={l}")

async def render(l='/dashboard', response=None):
    iv = Variable("")   # display name
    pv = Variable("")   # password
    ie = Variable("")
    pe = Variable("")   # password error
    widgets = []
    async def sp():
        for i in widgets:
            i.set_enabled(False)
        try: await lgn(iv, pv, ie, pe, l)
        finally:
            for i in widgets:
                i.set_enabled(True)
    with Col().classes("w-full h-full justify-center items-center"):
        with Card().classes("w-full sm:w-[90vw] md:w-[50vw] lg:w-[30vw] h-fit"):
            Label("LogIn").classes("text-lg border-b-2 w-full font-bold text-center")
            with RawCol().classes("w-full h-full gap-2"):
                with RawRow().classes("w-full justify-center text-sm"):
                    Label("Name/Email").classes("w-fit")
                    AddSpace()
                    Label(model=ie, model_configs=dict(strict=False)).classes("w-fit")\
                        .bind_visibility_from(ie, "value")
                widgets.append(Input(iv).classes("w-full"))

                with RawRow().classes("w-full justify-center text-sm"):
                    Label("Password").classes("w-fit")
                    AddSpace()
                    Label(model=pe, model_configs=dict(strict=False)).classes("w-fit")\
                        .bind_visibility_from(pe, "value")
                widgets.append(Password(model=pv).classes("w-full"))
                
                btn = Button("LogIn", on_click=sp)
                btn2 = Button("SignUp", config=dict(color='secondary'), link=f"/signup?redirectTo={l}")
                widgets.append(btn)
                widgets.append(btn2)
