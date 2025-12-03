from os import path, environ
from nicegui import ui, app
import uuid

PROD = False

HOST = '0.0.0.0'
PORT = int(environ.get("PORT", 8080))
SECRET = str(uuid.uuid4().hex)

NAME = "TurtleGraphics"
ICON = "🐢"

THEME = {
    "primary": "",
    "secondary": "",
    "accent": "",
}