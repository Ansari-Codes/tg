import math
from database.helpers import randomstr

class Screen:
    def __init__(self):
        self._width = 800
        self._height = 500
        self._bgcolor = "white"
        self._dpi = 1
        self._js_actions = []
        self._delay = 0
        self._animated = True
    def setDelay(self, delay):
        if delay < 0:
            raise ValueError("Delay must be a positive number!")
        self._delay = delay
        return delay
    def setSize(self, width, height=0):
        if not (width or isinstance(width, (int, float)) or width > 10):
            raise ValueError("Width must be a number greater than 10")
        if not height:
            height = width
        if not (height or isinstance(height, (int, float)) or height > 10):
            raise ValueError("Height must be a number greater than 10")
        self._width = width
        self._height = height
        self._js_actions.append(
            f"if (!window.is_running) return;"
            f"canvas.width = {width} * {self._dpi}; "
            f"canvas.height = {height} * {self._dpi};"
        )
        return width, height
    def setBg(self, color):
        self._bgcolor = color
        self._js_actions.append(
            f"canvas.style.background = '{color}';"
        )
        return color
    def setDpi(self, dpi):
        if not (dpi or isinstance(dpi, (int, float)) or dpi > 10):
            raise ValueError("DPI must be a number greater than 10")
        self._dpi = dpi
        self._js_actions.append(
            f"if (!window.is_running) return;"
            f"canvas.style.width = '{self._width}px'; "
            f"canvas.style.height = '{self._height}px'; "
            f"canvas.width = {self._width} * {dpi}; "
            f"canvas.height = {self._height} * {dpi};"
        )
        return dpi
    def getSize(self):
        return self._width, self._height
    def getBg(self): return self._bgcolor
    def getDpi(self): return self._dpi
    def getDelay(self): return self._delay
    def wait(self, ms=0):
        if ms < 0:raise ValueError("MilliSeconds `ms` must be a positive number!")
        self._js_actions.append(f"await delay({ms})")
    def clear(self):
        self._js_actions.append(
            "canvas.getContext('2d').clearRect(0,0,canvas.width,canvas.height);"
        )
    def grid(self, x_spacing=25, y_spacing=25, color="#ddd"):
        """optional: draw a background grid"""
        self._js_actions.append(
            f"""
            if (!window.is_running) return;
            let gctx = canvas.getContext('2d');
            gctx.beginPath();
            gctx.strokeStyle='{color}';
            for (let x=0; x<canvas.width; x+={x_spacing}) {{
                gctx.moveTo(x,0);
                gctx.lineTo(x,canvas.height);
            }}
            for (let y=0; y<canvas.height; y+={y_spacing}) {{
                gctx.moveTo(0,y);
                gctx.lineTo(canvas.width,y);
            }}
            gctx.stroke();
            """
        )

class T:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._angle = 0
        self._pen = True
        self._color = "black"
        self._width = 1
        self._delay = 0
        self._name = "turtle_" + randomstr()
        self._ctx = f"{self._name}_ctx"
        self._js_actions =  []
        self._animated = True

    # ----------------- JS Storage -----------------
    def getJsActions(self): return self._js_actions
    # ----------------- Movement -----------------
    def forward(self, distance):
        rad = math.radians(self._angle)
        new_x = self._x + distance * math.cos(rad)
        new_y = self._y + distance * math.sin(rad)
        if self._pen:
            self._js_actions.append(
                f"if (!window.is_running) return;"
                f"{f'await delay({self._delay});'*self.isAnimated()} "
                f"{self._ctx}.beginPath(); "
                f"{self._ctx}.moveTo(cx() + {self._x}, cy() + {self._y}); "
                f"{self._ctx}.lineTo(cx() + {new_x}, cy() + {new_y}); "
                f"{self._ctx}.strokeStyle='{self._color}'; {self._ctx}.lineWidth={self._width}; {self._ctx}.stroke();"
            )
        else:
            self._js_actions.append(
                f"{self._ctx}.moveTo(cx() + {new_x}, cy() + {new_y});"
            )
        self._x, self._y = new_x, new_y
    def backward(self, distance): self.forward(-distance)
    def right(self, angle): self._angle -= angle
    def left(self, angle): self._angle += angle
    def goto(self, x, y):
        if self._pen:
            self._js_actions.append(
                f"if (!window.is_running) return;"
                f"{f'await delay({self._delay});'*self.isAnimated()} "
                f"{self._ctx}.beginPath(); "
                f"{self._ctx}.moveTo(cx() + {self._x}, cy() + {self._y}); "
                f"{self._ctx}.lineTo(cx() + {x}, cy() + {y}); "
                f"{self._ctx}.strokeStyle='{self._color}'; {self._ctx}.lineWidth={self._width}; {self._ctx}.stroke();"
            )
        else:
            self._js_actions.append(f"{self._ctx}.moveTo(cx() + {x}, cy() + {y});")
        self._x, self._y = x, y
    def setHeading(self, angle):
        self._angle = angle
        return self._angle
    def getHeading(self): return self._angle
    # ----------------- Pen -----------------
    def up(self):
        self._pen = False
        return self._pen
    def down(self):
        self._pen = True
        return self._pen
    def isDown(self): return self._pen
    def setColor(self, color):
        self._color = color
        return self._color
    def getColor(self): return self._color
    def setLineWidth(self, w):
        self._width = w
        return self._width
    def getLineWidth(self): return self._width
    def clear(self): self._js_actions.append(f"{self._ctx}.clearRect(0, 0, cw(), ch());")
    def getPosition(self): return (self._x, self._y)
    
    # Animation related
    def isAnimated(self):
        return self._animated
    def animated(self):
        self._animated = True
        return self.isAnimated()
    def static(self):
        self._animated = False
        return self.isAnimated()
