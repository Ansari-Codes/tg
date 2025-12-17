from ENV import app, client

def getUserStorage() -> dict:
    response = client.get("/get/cookie")
    if response.status_code == 200:
        return response.json()
    return {}

def updateUserStorage(data: dict, clear=False) -> dict:
    user_id = data.get("id")
    if not user_id:
        raise ValueError("User ID is required to update storage.")
    response = client.post(f"/set/cookie/{user_id}")
    if response.status_code == 200:
        return {"success": True}
    return {"success": False, "error": response.text}

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

