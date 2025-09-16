from math import pi


class Figure:
    def __init__(self):
        pass

    @property
    def P(self) -> float:
        return 0

    @property
    def S(self) -> float:
        return 0


class Sircle(Figure):
    def __init__(self, radius: float):
        super().__init__()
        self.radius = radius

    @property
    def P(self) -> float:
        return 2 * pi * self.radius

    @property
    def S(self) -> float:
        return pi * self.radius * self.radius


class Rectangle(Figure):
    def __init__(self, width: float, height: float):
        super().__init__()
        self.width = width
        self.height = height

    @property
    def P(self) -> float:
        return (self.width + self.height) * 2

    @property
    def S(self) -> float:
        return self.width * self.height


class Square(Rectangle):
    def __init__(self, width: float):
        super().__init__(width, width)


class Triangle(Figure):
    def __init__(self, side_a, side_b, side_c):
        super().__init__()
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    @property
    def P(self) -> float:
        return self.side_a + self.side_b + self.side_c

    @property
    def S(self) -> float:
        half_P = self.P / 2
        return (half_P * (half_P - self.side_a) * (half_P - self.side_b) * (half_P - self.side_c)) ** 0.5
