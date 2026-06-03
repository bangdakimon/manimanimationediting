from manim import *


class SquareToCircle(Scene):
    def construct(self):
        square = Square()
        circle = Circle()
        circle.set_fill(opacity=0.5)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(circle))