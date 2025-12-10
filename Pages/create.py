from UI import Label, Header, Input, Button, TextArea, Dialog, SoftBtn, Col, Row, AddSpace, Html, Logger, ui
from UI.BASIC import Card, Notify, RawRow
from database.project import loadProject, updateProject, unique
from js import ZOOM_PAN
from storage import updateTabStorage as uts, getTabStorage as gts
from models import Variable
import cmath, math, random, statistics, numpy
import decimal, fractions, itertools, functools, collections, colorsys
import time, asyncio
from Turtle import T, Screen
from Runner import execute
from loading import showLoading

SAFE_MODULES = {
    'math': math, 'cmath': cmath, 'random': random, 'statistics': statistics,
    'numpy': numpy, 'asyncio': asyncio, 'decimal': decimal, 'fractions': fractions,
    'itertools': itertools, 'functools': functools, 'collections': collections,
    'colorsys': colorsys, 'time': time
}

def safe_import(name, *args, **kwargs):
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
    },
    'divmod': divmod, 'pow': pow, 'complex': complex
}

def exportCanvas():
    ui.run_javascript(f"""
    const canvas = document.getElementById("t-canvas");
    if (canvas) {{
        const link = document.createElement("a");
        link.download = "turtle-canvas-{random.randbytes(8).__str__()}.png";
        link.href = canvas.toDataURL("image/png");
        link.click();
    }}
    """)

async def save():
    project = gts()
    n = ui.notification("Saving", position="bottom-left", color='primary', spinner=True, timeout=100)
    await updateProject(project)
    n.dismiss()
    uts(project)
    Notify("Changes Saved!", color="success")

async def rename(d, title_model):
    project = gts()
    d.clear()
    w = []
    async def _rname():
        value = rinp.value.__str__().strip().lower()
        for i in w: i.disable()
        if not (await unique(value, "title")): Notify("Title already exists! Try different one!")
        else: 
            await updateProject({"id": gts().get("id"), "title": value})
            title_model.value = value
            project['title'] = value
            uts(project)
            d.close()
        for i in w: i.enable()
        Notify("Renamed!", color="success")
    with d:
        with Card():
            rinp = Input().classes("w-full")
            w.append(rinp)
            with RawRow().classes("w-full p-2 gap-2 items-center justify-between"):
                w.append(Button("Cancel", d.close, config=dict(color="red")))
                w.append(Button("Rename", _rname, config=dict(color="primary")))
    d.open()

async def publish(d,ss,b):
    project = gts()
    d.clear()
    w = []
    async def _publish():
        value = desc.value.__str__().strip().lower()
        for i in w: i.disable()
        await updateProject({"id": gts().get("id"), "description": value, "status": 1})
        project['description'] = value
        project['status'] = 1
        uts(project)
        for i in w: i.enable()
        ss.set_content("<span class='text-green-500'>Public</span>")
        ss.update()
        d.close()
        Notify("Your project is now public!", color="success")
        x = lambda _=None,d=d,s=ss:revertToDraft(d,s,b)
        b.set_text("Revert")
        b.on_click(x)
        await save()
    with d:
        with Card():
            desc = TextArea(autogrow=True, max_h="400px").classes("w-full")
            w.append(desc)
            with RawRow().classes("w-full p-2 gap-2 items-center justify-between"):
                w.append(Button("Cancel", d.close, config=dict(color="red")))
                w.append(Button("Publish", _publish, config=dict(color="primary")))
    d.open()

async def revertToDraft(d, ss, b):
    project = gts()
    d.clear()
    w = []
    async def _draft():
        for i in w: i.disable()
        await updateProject({"id": gts().get("id"), "status": 0})
        for i in w: i.enable()
        ss.set_content("<span class='text-yellow-500'>Draft</span>")
        project['status'] = 0
        ss.update()
        uts(project)
        d.close()
        Notify("Project reverted to draft!")
        x = lambda _=None,d=d,s=ss:publish(d,s,b)
        b.set_text("Publish")
        b.on_click(x)
        await save()
    with d:
        with Card():
            Label("Are you sure to revert your public project to draft?")
            with RawRow().classes("w-full p-2 gap-2 items-center justify-between"):
                w.append(Button("No", d.close, config=dict(color="red")))
                w.append(Button("Yes", _draft, config=dict(color="primary")))
    d.open()

async def clearCanvas():
    ui.run_javascript("""
const canvas = document.getElementById("t-canvas");
const ctx = canvas.getContext("2d");
ctx.setTransform(1, 0, 0, 1, 0, 0); 
ctx.clearRect(0, 0, canvas.width, canvas.height);
        """)

def copyCanvas():
    ui.run_javascript("""
const canvas = document.getElementById("t-canvas");
if (canvas) {
    canvas.toBlob(blob => {
        navigator.clipboard.write([
            new ClipboardItem({ "image/png": blob })
        ]);
    });
}
        """)

async def createFileMenu(d,tm,ss):
    with Button("File") as bbbb:
        project = gts()
        with ui.menu().classes("flex flex-col gap-1 p-2").props("auto-close"):
            Button("Save", save).classes("w-full")
            Button("Rename", lambda _=None,d=d,tm=tm:rename(d, tm)).classes("w-full")
            Button("Export Canvas", exportCanvas).classes("w-full")
            b = Button().classes("w-full")
            if project.get("status") in [1, "1"]:
                x = lambda _=None,d=d,s=ss:revertToDraft(d,s,b)
                b.set_text("Revert")
                b.on_click(x)
            else:
                x = lambda _=None,d=d,s=ss:publish(d,s,b)
                b.set_text("Publish")
                b.on_click(x)
    return bbbb
async def createEditMenu():
    with Button("Edit") as b:
        with ui.menu().classes("flex flex-col gap-1 p-2").props("auto-close"):
            Button("Copy Canvas", copyCanvas).classes("w-full")
            Button("Clear Canvas", clearCanvas).classes("w-full")
    return b
async def render(slug):
    c = showLoading("Editor")
    context = ui.context.client
    dialog = Dialog()
    await context.connected()
    projec = await loadProject(slug)
    project:dict = projec.data
    project['status'] = project.get("status", "0").__str__()
    uts(project)
    isSmallScreen = int(await ui.run_javascript("window.innerWidth")) < 500
    code = Variable()

    def print_(*args, end="\n", classes="", props="", style=""):
        content = ' '.join([str(i) for i in args])
        log.print(content, classes, props, style)
        return None
    itsglobal['__builtins__']['print'] = print_
    async def run():
        if not code.value.strip(): return
        shared = []
        class Turtle(T):
            def __init__(self):
                super().__init__()
                self._js_actions = shared
                self.screen = screen
                self._delay = screen._delay
                shared.append(f"const {self._ctx} = canvas.getContext('2d');{self._ctx}.setTransform(1, 0, 0, 1, 0, 0);")
        screen = Screen()
        screen._js_actions = shared
        safe_globals = {**itsglobal, "Screen":screen, "Turtle":Turtle}
        out, err, e = await execute(code.value, safe_globals)
        js = ''
        for l in shared:js += '\n' + l.strip()
        await asyncio.sleep(0.1)
        js = 'console.log("Starting turtle drawing...");\n' + js
        js += '\nconsole.log("Turtle drawing completed");'
        wrapped_js = f"""
        window.is_running = false;
        (async function() {{
            const canvas = document.getElementById('t-canvas');
            if (!canvas) {{
                console.error('Canvas not found');
                return;
            }}
            async function delay(ms){{return new Promise(r=>setTimeout(r,ms));}}
            window.is_running = true;
            let cw = () => canvas.width;
            let ch = () => canvas.height;
            let cx = () => cw() / 2;
            let cy = () => ch() / 2;
            {js}
            window.is_running = false;
        }})();
        """
        uts({"jscode": wrapped_js, "pycode": code.value})
        ui.run_javascript(wrapped_js)
        if out: print_(out)
        if err: print_(err)
        if e: print_(e)
    tm = Variable()
    tm.value = project.get("title","UnTitled")
    sss = lambda x:"<span class='text-yellow-500'>Draft</span>" if not float(x) else "<span class='text-green-500'>Public</span>"
    ss = Html(sss(project.get("status"))).classes("truncate text-lg h-full font-bold")
    with Header().classes("flex flex-row items-center") as header:
        if not isSmallScreen:
            await createFileMenu(dialog, tm, ss)
            await createEditMenu()
            Button("Run", run)
            Button("Stop", lambda: ui.run_javascript("window.is_running = false;"))
        else:
            with Button(config=dict(icon="menu")):
                with ui.menu().props("auto-close"):
                    (await createFileMenu(dialog, tm, ss)).classes("w-full")
                    (await createEditMenu()).classes("w-full")
                    Button("Run", run).classes("w-full")
                    Button("Stop", lambda: ui.run_javascript("window.is_running = false;")).classes("w-full")
        Label("", tm,
            model_configs=dict(forward=lambda x: x.title())
        ).classes("truncate text-lg h-full font-bold")
    ss.move(header)
    with ui.splitter().classes("w-full h-[84vh] p-0 m-0") as s:
        with s.before:
            with ui.splitter(horizontal=True).classes("w-full h-full") as sp:
                with sp.before:
                    t = ui.codemirror(
                    project.get("pycode", ""),
                    language='Python',
                    highlight_whitespace=True,
                    theme="githubLight"
                ).classes("w-full h-full")
                    t.bind_value(code)
                    code.value = project.get('pycode') #type:ignore
                with sp.after:
                    log = Logger().classes("bg-blue-100 dark:bg-primary w-full h-full")
        with s.after:
            Html("""
            <div id="canvas-wrapper" 
                class="bg-gray-400 dark:bg-gray-800"
                style="width:100%; height:100%; overflow:hidden; position:relative;">
                <canvas id="t-canvas" width="1200" height="800"
                        style="transform-origin: 0 0; background:white;"></canvas>
            </div>
            """)
            ZOOM_PAN()
    ui.run_javascript(project.get("jscode",""))
    c.delete()