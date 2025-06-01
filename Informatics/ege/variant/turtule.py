import turtle

screen = turtle.Screen()
screen.setup(width=600, height=600)

pen = turtle.Turtle()

pen.right(90)
for _ in range(7):
    pen.right(45)
    pen.forward(11)
    pen.right(45)

screen.mainloop()