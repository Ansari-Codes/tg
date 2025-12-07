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
            Html('<canvas class="w-full h-full bg-gray-50" id="t-canvas" ></canvas>').classes("w-full h-full")
