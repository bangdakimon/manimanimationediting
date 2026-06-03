from manim import *


class SquareToCircle(Scene):
    def construct(self):
        square = Square()
        circle = Circle()
        circle.set_fill(opacity=0.5)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(circle))

class HelloMath(Scene):
    def construct(self):
        text = Text("Gabut tapi produktif")
        formula = MathTex(r"E = mc^2").next_to(text, DOWN)

        self.play(Write(text))
        self.play(Write(formula))
        self.wait(1)