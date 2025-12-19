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
// -----------------------------------------------

// For panning with one finger
let lastTouchX, lastTouchY;

wrapper.addEventListener("touchstart", (e) => {
    if (e.touches.length === 1) {  // single finger → pan
        isPanning = true;
        lastTouchX = e.touches[0].clientX - originX;
        lastTouchY = e.touches[0].clientY - originY;
    }
});

wrapper.addEventListener("touchmove", (e) => {
    if (!isPanning || e.touches.length !== 1) return;
    e.preventDefault(); // prevent scrolling

    originX = e.touches[0].clientX - lastTouchX;
    originY = e.touches[0].clientY - lastTouchY;

    canvas.style.transform = `translate(${originX}px, ${originY}px) scale(${scale})`;
});

wrapper.addEventListener("touchend", () => {
    isPanning = false;
});

// For pinch zoom (two fingers)
let initialDistance = 0;
wrapper.addEventListener("touchstart", (e) => {
    if (e.touches.length === 2) {
        isPanning = false; // disable single-finger pan
        const dx = e.touches[0].clientX - e.touches[1].clientX;
        const dy = e.touches[0].clientY - e.touches[1].clientY;
        initialDistance = Math.hypot(dx, dy);
    }
});

wrapper.addEventListener("touchmove", (e) => {
    if (e.touches.length === 2) {
        e.preventDefault();
        const dx = e.touches[0].clientX - e.touches[1].clientX;
        const dy = e.touches[0].clientY - e.touches[1].clientY;
        const newDistance = Math.hypot(dx, dy);

        const zoomFactor = newDistance / initialDistance;
        scale *= zoomFactor;
        scale = Math.max(0.2, Math.min(scale, 5));

        // Update distance for next move
        initialDistance = newDistance;

        canvas.style.transform = `translate(${originX}px, ${originY}px) scale(${scale})`;
    }
});

""")