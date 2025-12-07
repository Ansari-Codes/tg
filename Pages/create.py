from UI import Label, Header, Input, Button, TextArea, SoftBtn, Col, Row, AddSpace, Html, Logger, ui
from database.project import loadProject
from storage import updateTabStorage as uts, getTabStorage as gts
from models import Variable
import cmath, math, random, statistics, numpy
import decimal, fractions, itertools, functools, collections, colorsys
import time, asyncio
from Turtle import Turtle
from Runner import execute
SAFE_MODULES = {
    'math': math, 'cmath': cmath, 'random': random, 'statistics': statistics,
    'numpy': numpy, 'asyncio': asyncio, 'decimal': decimal, 'fractions': fractions,
    'itertools': itertools, 'functools': functools, 'collections': collections,
    'colorsys': colorsys, 'time': time
}

def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name in SAFE_MODULES:
        return SAFE_MODULES[name]
    raise ImportError(f"Module '{name}' not found in environment!")

itsglobal = {
    '__builtins__': {
        'range': range, 'enumerate': enumerate,
        'int': int, 'float': float, 'str': str, 'bool': bool, 'list': list,
        'tuple': tuple, 'dict': dict, 'set': set, 'len': len, 'sum': sum,
        'min': min, 'max': max, 'abs': abs, 'round': round, 'zip': zip,
        'map': map, 'filter': filter, 'all': all, 'any': any,
        'sorted': sorted, 'reversed': reversed, 'isinstance': isinstance,
        'type': type, '__import__': safe_import, 'chr': chr, 'ord': ord,
        'bin': bin, 'oct': oct, 'hex': hex, 'id': id, 'format': format,
        'slice': slice, 'dir': dir, 'True': True, 'False': False, 'None': None,
        'Exception': Exception, 'ValueError': ValueError, 'TypeError': TypeError,
        'ZeroDivisionError': ZeroDivisionError, 'now_sec': time.time,
        'time_sec': time.perf_counter, 'strftime': time.strftime,
        'Turtle': Turtle
    },
    'divmod': divmod, 'pow': pow, 'complex': complex
}

async def render(slug):
    project = await loadProject(slug)
    project = project.data
    context = ui.context.client
    await context.connected()
    uts(project)
    with Header():
        Label("Create").classes("text-lg font-bold")
        AddSpace()
        Button("Run")
        Input()
        Button("Save")
    
    code = Variable()

    def print_(*args, end="\n", classes="", props="", style=""):
        content = ' '.join([str(i) for i in args])
        log.print(content, classes, props, style)
        return None
    itsglobal['__builtins__']['print'] = print_
    async def run():
        safe_globals = {**itsglobal}
        out, err, e = await execute(code.value, safe_globals)
        turtles = [v for v in safe_globals.values() if isinstance(v, Turtle)]
        js = ''
        for t in turtles:js += '\n'+t.getJs()
        ui.run_javascript(js)
        if out:print_(out)
        if err:print_(err)
        if e:print_(e)
    with ui.splitter().classes("w-full h-[84vh] p-0 m-0") as s:
        with s.before:
            with ui.splitter(horizontal=True).classes("w-full h-full") as sp:
                with sp.before:TextArea(
                    project.get("pycode", ""), 
                    code,
                    autogrow=True,
                    inp_cls="border-0 hover:border-0"
                ).classes("w-full h-full pr-2 border-0 hover:border-0")
                with sp.after:
                    log = Logger()
        with s.after:
            Button("Run", run)
            Html("""
            <div id="canvas-wrapper" 
                style="width:100%; height:100%; overflow:hidden; position:relative; background:#f0f0f0;">
                <canvas id="t-canvas" width="1200" height="800" 
                        style="transform-origin: 0 0; background:white;"></canvas>
            </div>
            """)
            ui.run_javascript("""
const wrapper = document.getElementById("canvas-wrapper");
const canvas = document.getElementById("t-canvas");

let scale = 1;        // zoom level
let originX = 0;      // pan X
let originY = 0;      // pan Y
let isPanning = false;
let startX, startY;

// ---------- Zoom ----------
wrapper.addEventListener("wheel", (e) => {
    e.preventDefault();
    const zoomStrength = 0.1;

    if (e.deltaY < 0) scale += zoomStrength;  // zoom in
    else scale -= zoomStrength;               // zoom out

    scale = Math.max(0.2, Math.min(scale, 5));  // limit zoom

    canvas.style.transform = `translate(${originX}px, ${originY}px) scale(${scale})`;
});

// ---------- Mouse Down → Start Panning ----------
wrapper.addEventListener("mousedown", (e) => {
    isPanning = true;
    startX = e.clientX - originX;
    startY = e.clientY - originY;
});

// ---------- Mouse Move → Panning ----------
wrapper.addEventListener("mousemove", (e) => {
    if (!isPanning) return;

    originX = e.clientX - startX;
    originY = e.clientY - startY;

    canvas.style.transform = `translate(${originX}px, ${originY}px) scale(${scale})`;
});

// ---------- Mouse Up → Stop Panning ----------
wrapper.addEventListener("mouseup", () => isPanning = false);
wrapper.addEventListener("mouseleave", () => isPanning = false);
""")