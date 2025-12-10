# ui file (snippet)
from UI import Card, Center, Input, SoftBtn, Label, Row, Col, RawCol, RawRow, AddSpace, CheckBox, Notify, Button, navigate
from models import Variable
from database.auth import signup
from storage import getUserStorage, updateUserStorage

def validate(nv, mv, pv, cv, ne, me, pe):
    """
    Returns True when inputs are valid (no errors).
    Also sets .value on the error Variables to error messages when present.
    """
    # clear previous errors
    ne.value = ""
    me.value = ""
    pe.value = ""

    name = nv.value.strip().lower()
    mail = mv.value.strip().lower()
    pswd = pv.value.strip()
    cnfm = cv.value.strip()

    has_error = False

    if not name:
        ne.value = "Username is required!"
        has_error = True

    if not mail:
        me.value = "Mail is required!"
        has_error = True

    if not pswd:
        pe.value = "Password is required!"
        has_error = True

    # if there were missing required fields, return False
    if has_error:
        return False

    if not cnfm:
        pe.value = "Confirm is required!"
        return False

    if pswd != cnfm:
        pe.value = "Passwords do not match!"
        return False

    # all checks passed
    return True

async def sup(nv, mv, pv, cv, ne, me, pe, l):
    if not validate(nv, mv, pv, cv, ne, me, pe):
        return

    name = nv.value.strip().lower()
    mail = mv.value.strip().lower()
    pswd = pv.value.strip()

    res = await signup(name, mail, pswd)
    if not res.success:
        # map server-side errors to error Variables so UI shows them
        if 'name' in res.errors:
            ne.value = res.errors['name']
        if 'mail' in res.errors:
            me.value = res.errors['mail']
        if 'pswd' in res.errors:
            pe.value = res.errors['pswd']
        if 'other' in res.errors:
            Notify(res.errors.get("other", "An unknown error occured!"), type='negative')
        return

    # success UI feedback (you can customize)
    res.data['auth'] = True
    print("SignUp:", res.data)
    updateUserStorage(res.data)
    Notify("Account created!", type='positive')
    navigate(l)

async def render(l='/dashboard'):
    nv = Variable("")   # display name
    mv = Variable("")   # email
    pv = Variable("")   # password
    cv = Variable("")   # confirm password
    ne = Variable("")   # name error
    me = Variable("")   # mail error
    pe = Variable("")   # password error
    widgets = []
    async def sp():
        for i in widgets:
            i.set_enabled(False)
        try: await sup(nv, mv, pv, cv, ne, me, pe, l)
        finally:
            for i in widgets:
                i.set_enabled(True)
    with Col().classes("w-full h-full justify-center items-center"):
        with Card().classes("w-full sm:w-[90vw] md:w-[50vw] lg:w-[30vw] h-fit"):
            Label("SignUp").classes("text-lg border-b-2 w-full font-bold text-center")
            with RawCol().classes("w-full h-full gap-2"):
                with RawRow().classes("w-full justify-center text-sm"):
                    Label("Display Name *").classes("w-fit")
                    AddSpace()
                    Label(model=ne, model_configs=dict(strict=False)).classes("w-fit")\
                        .bind_visibility_from(ne, "value")
                widgets.append(Input(nv).classes("w-full"))

                with RawRow().classes("w-full justify-center text-sm"):
                    Label("Email *").classes("w-fit")
                    AddSpace()
                    Label(model=me, model_configs=dict(strict=False)).classes("w-fit")\
                        .bind_visibility_from(me, "value")
                widgets.append(Input(mv).classes("w-full"))

                with RawRow().classes("w-full justify-center text-sm"):
                    Label("Password *").classes("w-fit")
                    AddSpace()
                    Label(model=pe, model_configs=dict(strict=False)).classes("w-fit")\
                        .bind_visibility_from(pe, "value")
                widgets.append(Input(pv).classes("w-full"))
                widgets.append(Input(cv).classes("w-full"))

                checkbox = CheckBox("I accept agreements!").classes("w-full")
                widgets.append(checkbox)
                btn = Button("Create Account", on_click=sp)
                btn.bind_enabled_from(checkbox, "value").classes("w-full")
                btn2 = Button("LogIn", on_click=lambda:navigate(f"/login?redirectTo={l}"), config=dict(color='secondary'))
                widgets.append(btn2)
                widgets.append(btn)
