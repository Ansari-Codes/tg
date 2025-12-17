from os import path, environ
from nicegui import ui, app
from fastapi.testclient import TestClient
import uuid

PROD = False

HOST = '0.0.0.0'
PORT = int(environ.get("PORT", 8000))
SECRET = str("my-secret-key-is-that-with-fixed-host-but-random-port")
client = TestClient(app, f"http://localhost:{PORT}")

NAME = "TurtleGraphics"
ICON = "🐢"

THEME = {
    "primary": "#48815A",  
    "secondary": "#46925E",
    "accent": "#DFF6DD",   
    "dark": "#293126",     
    "positive": "#107C10", 
    "negative": "#A80000", 
    "info": "#017CBA",     
    "warning": "#FFB900",  
    "debug": "#6C757D",    
    "btn-l": "#3BA75A",    
    "btn-d": "#225532",    
    "card-l": "#F3FAF3",   
    "card-d": "#193519",   
}
