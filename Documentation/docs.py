from UI import Button, Label, Html, Link, Header, ui, AddSpace

# --------------------------------------------------
# Docs registry
# --------------------------------------------------
sections = {
    "Introduction": ("Documentation/mds/intro.md", "info"),
    "Dashboard": ("Documentation/mds/dashboard.md", "dashboard"),
    "Editor": ("Documentation/mds/create.md", "table_chart"),
    "TurtleAPI": ("Documentation/mds/turtle.md", "code"),
    "About The Developer": ("Documentation/mds/about.md", "logo_dev"),
    "GitHUB": ("Github", "commit"),
}

# --------------------------------------------------
# Global cache (loaded once)
# --------------------------------------------------
DOC_CACHE: dict[str, str | None] = {}

def preload_docs():
    for _, (src, key) in sections.items():
        if src.endswith(".md"):
            try:
                with open(src, "r", encoding="utf-8") as f:
                    DOC_CACHE[key] = f.read()
            except FileNotFoundError:
                DOC_CACHE[key] = "❌ Documentation not found"
        else:
            DOC_CACHE[key] = None

preload_docs()

# --------------------------------------------------
# Header
# --------------------------------------------------
async def create_header(drawer):
    with ui.header().classes("items-center justify-between") as h:
        Label("🐢 TurtleGraphics / Docs").classes("text-lg font-bold")
        AddSpace()
        Button("Home", link="/")
        Button("Explore", link="/explore")
        Button("Docs").on_click(drawer.toggle)
    return h

# --------------------------------------------------
# Docs page (single scrollable element)
# --------------------------------------------------
def create_docs_content():
    """Creates all sections at once in a scrollable container"""
    container = ui.scroll_area().classes("w-full text-[16px] leading-relaxed h-[86vh]")

    section_elements = {}
    with container:
        for title, (_, key) in sections.items():
            with ui.element().classes("flex flex-col") as sec:
                sec.props(f"id='{key}'")
                with ui.element().classes("flex flex-row gap-2 items-center border-b-2"):
                    ui.icon(key, size="md", color='primary')
                    ui.label(title).classes("text-2xl font-bold")
                content = DOC_CACHE.get(key)
                if content is None:
                    ui.link(
                        "Open GitHub Repository",
                        "https://github.com/Ansari-Codes/tg"
                    ).classes("text-blue-600 underline text-xl")
                else:
                    ui.markdown(content).classes("text-md")
            section_elements[key] = sec

    return container, section_elements

# --------------------------------------------------
# Drawer (scrolls to section)
# --------------------------------------------------
async def create_drawer(content_area, section_elements):
    with ui.left_drawer(value=True).classes("bg-gray-100") as drawer:
        with ui.element().classes("w-full flex flex-col gap-1"):
            for title, (_, key) in sections.items():
                Button(title, config=dict(icon=key), link=f'#{key}')\
                    .classes("w-full justify-start")\
                    .props('align="left" ')
    return drawer

# --------------------------------------------------
# Docs page entry point
# --------------------------------------------------
async def create_docs():
    content_area, section_elements = create_docs_content()
    drawer = await create_drawer(content_area, section_elements)
    await create_header(drawer)
