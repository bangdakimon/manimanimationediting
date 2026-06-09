from manim import *

class TestManim(Scene):
    def construct(self):
        title = Text("Manim works on Windows!")
        self.play(Write(title))
        self.wait(1)