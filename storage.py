from ENV import app

def _ensure(key: str):
    if key not in app.storage.user:
        app.storage.user[key] = {}
    return app.storage.user[key]

def getUserStorage()->dict:return _ensure("user")
def updateUserStorage(data: dict, clear=False)->dict:
    user = _ensure("user")
    if clear:user.clear()
    user.update(data)
    return user

def getThemeStorage()->dict:return _ensure("theme")
def updateThemeStorage(data: dict, clear=False)->dict:
    theme = _ensure("theme")
    if clear:theme.clear()
    theme.update(data)
    return theme
