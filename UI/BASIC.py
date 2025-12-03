from ENV import ui, THEME
from typing import Callable, Literal

def navigate(link:str,new_tab:bool=False):ui.navigate.to(link,new_tab)

def Label(text="", model=None, model_configs=None):
    lbl = ui.label(text)
    if model:
        model_configs = model_configs or {}
        lbl.bind_text(model, target_name='value', **model_configs)
    return lbl

def Header(): return ui.header(fixed=True, elevated=False)
def Html(html: str): return ui.html(html, sanitize=lambda x:x)
def Col(): return ui.column()
def Row(): return ui.row()
def RawCol(): return ui.element().classes("flex flex-col")
def RawRow(): return ui.element().classes("flex flex-row")
def Center(): return ui.element( ).classes("flex justify-center items-center" )
def Footer(config: dict|None = None): return ui.footer(**(config or {}))
def Card(align: Literal['start', 'end', 'center', 'baseline', 'stretch']|None = None ):
    return ui.card(align_items=align)

def Link(
        text: str = "",
        link: str = "",
        underline:  bool = True,
        new_tab: bool = False,
    ):
    return ui.link(text, link, new_tab).classes("hover:underline"*underline )

def SoftBtn(
        text: str = "",
        on_click: Callable = lambda: (),
        link: str = "",
        new_tab: bool = False,
        icon: str = "",
        icon_config: dict|None = None,
        icon_side: Literal['r', 'l'] = 'l',
        px: int = 4,
        py: int = 2,
        clr: str = "btn",
        ripple: bool = True,
        hover_effects: bool = True,
        active_effects: bool = True,
        text_align: Literal['left', 'center', 'right'] = 'center',
        rounded: Literal['none', 'xs', 'sm', 'md', 'lg', 'xl', '2xl', 'full']|None = 'sm',
        justify: Literal['center', 'between', None] = 'center',
        text_clr: str = "",
    ):
    colors = list(THEME.keys())
    c = clr or "transparent"
    tc = text_clr or "white"
    if c not in colors+['transparent']: c = f"[{c}]"
    if tc not in colors+['transparent']: tc = f"[{tc}]"
    icon_config = icon_config or {}
    base_classes = (
        f"flex items-center{' justify-'+justify if justify else ''} gap-0 text-{text_align or 'center'} "
        f"px-{px} py-{py} rounded-{rounded or 'none'} text-{tc} text-[14px] font-medium "
        f"transition-all duration-200 ease-in-out "
        f"bg-{c} shadow-md {'hover:shadow-lg'*bool(hover_effects)} {'active:scale-95'*bool(active_effects)} "
        f"select-none cursor-pointer {'ripple'*bool(ripple)} no-underline"
    )
    classes = f"{base_classes}".strip()
    with (ui.link("", link, new_tab) if link else Row()).classes(classes) as btn:
        if icon and icon_side == 'l':
            ui.icon(icon, **icon_config).classes(f"text-[18px]")
        if text:
            ui.label(text)
        if icon and icon_side == 'r':
            ui.icon(icon, **icon_config).classes(f"text-[18px]")
    btn = btn.on('click', on_click)
    return btn

def Input(
        model = None,
        default_props: bool|None = True,
        bindings: dict|None = None,
        type: Literal['text', 'color', 'number'] = 'text',
        **kwargs
    ):
    bindings = bindings or {}
    inp = None
    if type == "text": inp = ui.input(**kwargs)
    elif type == "color": inp = ui.color_input(**kwargs)
    elif type == 'number': inp = ui.number(**kwargs)
    if inp:
        inp.classes("bg-inp rounded-sm")
        inp.props('input-class="text-text-secondary"')
        inp.props("dense outlined"*bool(default_props) + ' ')
        if model: inp.bind_value(model, 'value', **bindings)
    return inp

def Select(
        model = None,
        options: list|dict|None = None,
        default_props: bool|None = True,
        bindings: dict|None = None,
        **kwargs
    ):
    bindings = bindings or {}
    slc = ui.select(options=options or [], **kwargs)
    slc.props("dense outlined"*bool(default_props) + ' ')
    if model: slc.bind_value(model, 'value', **bindings)
    slc.classes("bg-inp rounded-sm").props('input-class="text-text-secondary"')
    return slc

def Button(
        text: str = "", 
        on_click = lambda: (),
        config: dict|None = None
    ):
    if not config: config = {}
    return ui.button(text=text, on_click=on_click, **config).props("unelevated push")

def TextArea(
        content: str = "",
        model=None,
        autogrow: bool = False,
        max_h: str|None = None,
        min_h: str|None = None,
        overflow: str|None = None,
        flexible: bool = False,
        config: dict|None = None
    ):
    if not config: config = {}
    ta = ui.input(value=content, **config)
    inner_classes = ""
    if model: ta.bind_value(model)
    if flexible: inner_classes += " flex-grow flex-shrink resize-none"
    if min_h: inner_classes += f" min-h-[{min_h}]"
    if max_h: inner_classes += f" max-h-[{max_h}]"
    if overflow: inner_classes += f" overflow-{overflow}"
    if autogrow: ta.props('autogrow')
    ta.classes(inner_classes)
    ta.props('dense outlined')
    ta.classes("bg-inp rounded-sm").props('input-class="text-text-secondary"')
    return ta

def CheckBox(
        text:str = "",
        value:bool = False,
        on_change:Callable = lambda x:()
    ):
    return ui.checkbox(text, value=value, on_change=on_change)

def AddSpace():
    return ui.space()

def Icon(
        name: str = "" , 
        size: str|None = None,
        color: str|None = None,
    ):
    return ui.icon(name, size=size, color=color)

def Notify(
        message:str = '', 
        position:Literal['top-left', 'top-right', 'bottom-left', 
                         'bottom-right', 'top', 'bottom', 'left', 
                         'right', 'center'
                        ]='top-right',
        close_button='✖', 
        **kwargs
    ): ui.notify(message, position=position, close_button=close_button, **kwargs)

def DialogHeader(
        title: str = "",
        close_icon: str|bool = True,
        close_text: str = "",
        on_close: Callable|None = None,
        close_config: dict|None = None,
        dialog: ui.dialog|None = None,
    ):
    close_config = close_config or {}
    icon_to_show = None
    if isinstance(close_icon, str):
        icon_to_show = close_icon.strip() if close_icon.strip() else ""
    else:
        icon_to_show = "close" * close_icon
    with Row().classes("w-full bg-secondary dark:bg-primary justify-between p-2 items-center justify-between gap-2") as header_:
        title_ = Label(title).classes("text-2xl font-medium text-white")
        close_btn_ = None
        if (close_icon or close_text):
            close_btn_ = SoftBtn(
                close_text,
                on_click=on_close or (lambda:()),
                icon=icon_to_show,
                rounded='sm' if (not icon_to_show) and (close_text) else "full",
                clr='error',
                px=1,
                py=1,
                **close_config
            ).classes(f"border-2 border-red-300 shadow-none")
    if dialog: header_.move(dialog, 0)
    return header_

def Dialog():
    return ui.dialog().props('backdrop-filter="hue-rotate(10deg)"')
