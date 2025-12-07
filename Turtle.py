import math

class Turtle:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._angle = 0
        self._pen = True
        self._color = "black"
        self._width = 1
        self._js_actions = []

    # ----------------- JS Storage -----------------
    def getJsActions(self): return self._js_actions

    # ----------------- Movement -----------------
    def forward(self, distance):
        rad = math.radians(self._angle)
        new_x = self._x + distance * math.cos(rad)
        new_y = self._y + distance * math.sin(rad)
        if self._pen:
            self._js_actions.append(
                f"ctx.beginPath(); "
                f"ctx.moveTo(cx() + {self._x}, cy() + {self._y}); "
                f"ctx.lineTo(cx() + {new_x}, cy() + {new_y}); "
                f"ctx.strokeStyle='{self._color}'; ctx.lineWidth={self._width}; ctx.stroke();"
            )
        else:
            self._js_actions.append(
                f"ctx.moveTo(cx() + {new_x}, cy() + {new_y});"
            )
        self._x, self._y = new_x, new_y
    def backward(self, distance): self.forward(-distance)
    def right(self, angle): self._angle -= angle
    def left(self, angle): self._angle += angle
    def goto(self, x, y):
        if self._pen:
            self._js_actions.append(
                f"ctx.beginPath(); "
                f"ctx.moveTo(cx() + {self._x}, cy() + {self._y}); "
                f"ctx.lineTo(cx() + {x}, cy() + {y}); "
                f"ctx.strokeStyle='{self._color}'; ctx.lineWidth={self._width}; ctx.stroke();"
            )
        else:
            self._js_actions.append(f"ctx.moveTo(cx() + {x}, cy() + {y});")
        self._x, self._y = x, y
    def setHeading(self, angle):
        self._angle = angle
        return self._angle
    def getHeading(self): return self._angle
    # ----------------- Pen -----------------
    def setPen(self, value: bool):
        self._pen = bool(value)
        return self._pen
    def getPen(self): return self._pen
    def setColor(self, color):
        self._color = color
        return self._color
    def getColor(self): return self._color
    def setLineWidth(self, w):
        self._width = w
        return self._width
    def getLineWidth(self): return self._width
    def clear(self): self._js_actions.append("ctx.clearRect(0, 0, cw(), ch());")

    # ----------------- Utility -----------------
    def getPosition(self): return (self._x, self._y)
    # ----------------- Generate JS -----------------
    def getJs(self):
        js_code = []
        js_code.extend(self._js_actions)
        return '\n'.join(js_code)

'''
t = Turtle()
for i in range(4):
    t.forward(90)
    t.left(90)
'''
