The **Turtle API** allows you to create drawings programmatically using Python in a simple and intuitive way. It is designed for **kids, beginners, and Python enthusiasts** to learn coding while creating visual artwork.

---

### Screen

The `Screen` class represents the drawing area (canvas) where all turtle drawings appear. You can customize it using the following methods:

* `setSize(width, height)`: Set the canvas width and height. If height is omitted, width is used for both dimensions.
* `setBg(color)`: Set the background color of the canvas.
* `setDpi(dpi)`: Adjust the resolution of the canvas.
* `getSize()`: Get the current width and height of the canvas.
* `getBg()`: Get the current background color.
* `clear()`: Clear all drawings from the canvas.
* `grid(x_spacing, y_spacing, color)`: Draw an optional grid on the canvas for guidance.

---

### Turtle

The `Turtle` class represents a turtle that moves around the canvas and draws lines. You can control its movement, pen state, color, and line width.

#### Movement

* `forward(distance)`: Move the turtle forward by a certain distance.
* `backward(distance)`: Move the turtle backward.
* `right(angle)`: Turn the turtle clockwise by a specified angle.
* `left(angle)`: Turn the turtle counterclockwise by a specified angle.
* `goto(x, y)`: Move the turtle to a specific coordinate.
* `setHeading(angle)`: Set the turtle’s direction (angle in degrees).
* `getHeading()`: Get the current heading of the turtle.

#### Pen Control

* `up()`: Lift the pen; the turtle moves without drawing.
* `down()`: Put the pen down; the turtle draws when moving.
* `isDown()`: Check if the pen is currently down.
* `setColor(color)`: Set the color of the pen.
* `getColor()`: Get the current pen color.
* `setLineWidth(width)`: Set the pen thickness.
* `getLineWidth()`: Get the current pen thickness.
* `clear()`: Clear all lines drawn by the turtle.

#### Position and Animation

* `getPosition()`: Get the current `(x, y)` position of the turtle.
* `animated()`: Enable smooth animated movement.
* `static()`: Disable animation (instant movement).
* `isAnimated()`: Check whether the turtle is animated.

---

This API provides a **simple, fun, and visual way to learn Python**, letting users experiment with loops, functions, and geometry while creating colorful drawings.