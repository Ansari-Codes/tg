from UI import Button, Label, Input, TextArea, Icon, Card, Row, Col, RawCol, RawRow, Html, ui
from nicegui.events import UploadEventArguments
import  base64

def sectionLabel(text):
    return Label(text).classes("w-full text-md font-semibold")

async def settings(area):
    # with ui.list():
    #     with ui.expansion("Account", caption="Configure your account info", icon='account_circle', group='settings'):
    #         sectionLabel("Here you can change your password...")
    #         with Col().classes("max-w-[500px]"):
    #             Input(label="Old Password")
    #             Input(label="New Password")
    #             Input(label="Confirm Password")
    #             Button("Change my password", config=dict(icon="check"))
    #     with ui.expansion("Profile", caption="Configure your profile", icon='info', group='settings'):
    #         sectionLabel("Tell breifly about yourself...")
    #         TextArea(autogrow=True, max_h="500px").classes("max-w-[500px] w-full")
    #         sectionLabel("Change your avatar here...")
    #         with Row():
    #             async def showAsImage(content: UploadEventArguments):
    #                 c = await content.file.read()
    #                 img_base64 = base64.b64encode(c).decode('utf-8')
    #                 img_src = f"data:{content.file.content_type};base64,{img_base64}"
    #                 ic.set_source(img_src)
    #             upl = ui.upload(label="Upload file here...", auto_upload=True, on_upload=showAsImage)
    #             ic = ui.interactive_image()
    Html("This page is currently in progress, will be available in future soon, <span class='font-bold'>InshAllah!</span>").classes("text-5xl font-light p-2 rounded-lg shadow-xl bg-primary")