from ..ENV import ui

def Label(text):
    ui.label(text)

def Header():
    return ui.header(fixed=True, elevated=False)