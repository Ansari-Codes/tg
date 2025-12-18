from ENV import app, client

def getUserStorage() -> dict:
    return {}

def updateUserStorage(data: dict, clear=False) -> dict:
    return {"success": False}

def clearUserStorage():updateUserStorage({},True)

def userID(): return getUserStorage().get("id")
def isAuth(): return getUserStorage().get("auth")
def getThemeStorage()->dict:
    return {}
def updateThemeStorage(data: dict, clear=False)->dict:
    theme = getThemeStorage()
    if clear:theme.clear()
    theme.update(data)
    return theme

def getTabStorage()->dict:return app.storage.tab
def updateTabStorage(data: dict, clear=False)->dict:
    tab = getTabStorage()
    if clear:tab.clear()
    tab.update(data)
    return tab

