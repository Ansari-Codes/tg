from UI import Label, Header, Input, Button, TextArea, Dialog, Col, Row, AddSpace, Html, Logger, ui, navigate
from UI.BASIC import Card, Notify, RawCol, RawRow
from database.project import loadProject, updateProject, unique
from database.session import getCurrentUser
from js import ZOOM_PAN
from models import Variable
import cmath, math, random, statistics, numpy
import decimal, fractions, itertools, functools, collections, colorsys
import time, asyncio
from Turtle import T, Screen
from Runner import execute
from loading import showLoading

SAFE_MODULES = {
    'math': math, 'cmath': cmath, 'random': random, 'statistics': statistics,
    'numpy': numpy, 'decimal': decimal, 'fractions': fractions,
    'itertools': itertools, 'functools': functools, 'collections': collections,
    'colorsys': colorsys
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
        'SyntaxError': SyntaxError,
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

async def rename(d, title_model, saver):
    d.clear()
    w = []
    async def _rname():
        value = rinp.value.__str__().strip().lower()
        for i in w: i.disable()
        if not (await unique(value, "title")): 
            Notify("Title already exists! Try different one!")
            for i in w: i.enable()
            return
        else: 
            await saver({"title": value})
            title_model.value = value
            d.close()
        for i in w: i.enable()
        Notify("Renamed!", color="success")
    with d:
        with Card():
            with RawCol().classes("w-full h-full gap-1"):
                Label("New Title here...").classes("w-full text-md font-semibold")
                rinp = Input().classes("w-full")
                w.append(rinp)
                with RawRow().classes("w-full gap-2 items-center justify-between"):
                    w.append(Button("Cancel", d.close, config=dict(color="red")))
                    w.append(Button("Rename", _rname, config=dict(color="primary")))
    d.open()

async def publish(d,ss,b,saver):
    d.clear()
    w = []
    async def _publish():
        value = desc.value.__str__().strip()
        for i in w: i.disable()
        await saver({"description": value, "status": 1})
        for i in w: i.enable()
        ss.set_content("<span class='text-green-500'>Public</span>")
        ss.update()
        d.close()
        Notify("Your project is now public!", color="success")
        x = lambda _=None,d=d,s=ss:revertToDraft(d,s,b,saver)
        b.set_text("Revert")
        b.on_click(x)
    with d:
        with Card():
            with RawCol().classes("w-full h-full gap-1"):
                Label("Description").classes("w-full text-md font-semibold")
                with RawRow().classes("w-full max-h-[400px]"):
                    desc = TextArea(autogrow=True).classes("w-full")
                w.append(desc)
                with RawRow().classes("w-full gap-2 items-center justify-between"):
                    w.append(Button("Cancel", d.close, config=dict(color="red")))
                    w.append(Button("Publish", _publish, config=dict(color="primary")))
    d.open()

async def revertToDraft(d, ss, b, saver):
    d.clear()
    w = []
    async def _draft():
        for i in w: i.disable()
        await saver({"status": 0})
        for i in w: i.enable()
        ss.set_content("<span class='text-yellow-500'>Draft</span>")
        d.close()
        Notify("Project reverted to draft!")
        x = lambda _=None,d=d,s=ss:publish(d,s,b,saver)
        b.set_text("Publish")
        b.on_click(x)
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

async def createFileMenu(d,tm,ss,saver,project):
    with Button("File") as bbbb:
        with ui.menu().classes("flex flex-col gap-1 p-2").props("auto-close"):
            Button("Save", saver).classes("w-full")
            Button("Rename", lambda _=None,d=d,tm=tm:rename(d, tm, saver)).classes("w-full")
            Button("Export Canvas", exportCanvas).classes("w-full")
            b = Button().classes("w-full")
            if project.get("status") in [1, "1"]:
                x = lambda _=None,d=d,s=ss:revertToDraft(d,s,b,saver)
                b.set_text("Revert")
                b.on_click(x)
            else:
                x = lambda _=None,d=d,s=ss:publish(d,s,b,saver)
                b.set_text("Publish")
                b.on_click(x)
    return bbbb

async def render(slug,token):
    c = showLoading("Editor")
    context = ui.context.client
    dialog = Dialog()
    await context.connected()
    res = await getCurrentUser(token)
    if not res.success:
        navigate("/login?redirectTo=/dashboard")
    if slug:
        projec = await loadProject(slug, withowner=True, owner=res.data.get("id"))
        project:dict = projec.data
        if not projec.success:
            c.delete()
            Label("Cannot load project!").classes("text-xl font-bold text-red-500")
            return
    else:
        project = {}
    isSmallScreen = int(await ui.run_javascript("window.innerWidth")) < 500
    code = Variable()
    jscode = Variable()
    def status_badge(status):
        return (
            "<span class='text-green-500'>Public</span>"
            if int(status) == 1
            else "<span class='text-yellow-500'>Draft</span>"
        )
    async def save(extra=None):
        extra = extra or {}
        pjt = {
            **project,
            "pycode": code.value.strip(),
            "jscode": jscode.value.strip(),
        }
        if "status" in extra:
            pjt["status"] = extra["status"]
        pjt.update(extra)
        n = ui.notification("Saving", position="bottom-left", color='primary', spinner=True, timeout=100)
        await updateProject(pjt)
        n.dismiss()
        Notify("Changes Saved!", color="success")
    async def run(_=None, thumbnail=False):
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
        def sleep__(ms: int):
            shared.append(f"await delay({ms});")
        def print_(*args, classes="", props="", style=""):
            content = ' '.join([str(i) for i in args])
            shared.append(f"print('{content}', '{classes}', '{props}','{style}')")
            return None
        safe_globals = {**itsglobal, "Screen":screen, "Turtle":Turtle, "sleep": sleep__, "print": print_}
        out, err, e = await execute(code.value, safe_globals)
        js = ''
        for l in shared:js += '\n' + l.strip()
        js_ = """
        (async function() {
            const canvas = document.getElementById("{{canvas}}");
            const logger = document.getElementById("t-logger");
            if (!canvas) {
                console.error('Canvas not found');
                return;
            }
            let thumbnail = {{thumbnail}};
            async function delay(ms){
                if (thumbnail) return;
                return new Promise(r=>setTimeout(r,ms));
            }
            async function print(msg, clas="", props="", styles=""){
                const p = document.createElement("p");
                p.className = clas;
                p.style.cssText = styles;
                p.innerHTML = msg;
                logger.appendChild(p);
                logger.scrollTop = logger.scrollHeight;
            }
            window.is_running = true;
            let cw = () => canvas.width;
            let ch = () => canvas.height;
            let cx = () => cw() / 2;
            let cy = () => ch() / 2;
            {{js}}
            console.log("Done");
        })();
        """
        wrapped_js = js_.replace("{{canvas}}", "t-canvas", 1).replace("{{thumbnail}}", thumbnail.__str__().lower()).replace("{{js}}", js, 1)
        jscode.value = js_.replace("{{js}}", js, 1)
        ui.run_javascript("window.is_running = false;" + wrapped_js)
        def printer_print(val, c="", p="", s=""):
            ui.run_javascript(f"""
            const logger = document.getElementById("t-logger");
            async function print(msg, clas="", props="", styles=""){{
                const p = document.createElement("p");
                p.className = clas;
                p.style.cssText = styles;
                p.innerHTML = msg;
                logger.appendChild(p);
                logger.scrollTop = logger.scrollHeight;
            }}
            print("{val}", "{c}", "{p}", "{s}")""")
        if out: printer_print(out)
        if err: printer_print(err, "text-red-500 font-bold")
        if e: printer_print(e, "text-lg text-yellow-800 font-bold")
    tm = Variable()
    tm.value = project.get("title","UnTitled")
    ss = Html(status_badge(project.get("status", 0))).classes("truncate text-lg h-full font-bold")
    with Header().classes("flex flex-row items-center") as header:
        if not isSmallScreen:
            await createFileMenu(dialog, tm, ss,save,project)
            Button("Clear Canvas", clearCanvas)
            Button("Run", run)
            Button("Stop", lambda: ui.run_javascript("window.is_running = false;"))
        else:
            with Button(config=dict(icon="menu")):
                with ui.menu():
                    (await createFileMenu(dialog, tm, ss,save,project)).classes("w-full")
                    Button("Clear Canvas", clearCanvas).classes("w-full")
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
                    theme="githubLight",
                    on_change=lambda x:code.set(x.value.__str__().strip())
                ).classes("w-full h-full")
                    code.value = project.get('pycode') #type:ignore
                with sp.after:
                    log = Html("<div class='bg-blue-100 dark:bg-primary w-full h-full' id='t-logger'></div>").classes("w-full h-full")
        with s.after:
            Html("""
<div id="canvas-wrapper" class="w-full h-full overflow-hidden bg-gray-200">
    <canvas id="t-canvas" 
            style="transform-origin: 0 0; background:white;">
    </canvas>
</div>
            """).classes("w-full h-full overflow-hidden")
            ZOOM_PAN()
    await run(thumbnail=True)
    c.delete()
