from UI import ui

ZOOM_PAN = lambda: ui.run_javascript("""
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