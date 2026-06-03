from manim import *
import random


class NgadipronoLogoIntro(Scene):
    def construct(self):
        # Background
        self.camera.background_color = "#0D0D0D"

        # ── PHASE 1: Equalizer bars animate in from silence ──
        num_bars = 21
        bar_width = 0.12
        bar_gap = 0.22
        total_width = num_bars * bar_gap
        eq_color_left = "#3E5F33"
        eq_color_right = "#56723E"

        bars = VGroup()
        for i in range(num_bars):
            x = -total_width / 2 + i * bar_gap
            bar = RoundedRectangle(
                width=bar_width,
                height=0.05,
                corner_radius=0.03,
            )
            # gradient color from dark green center to lighter green edges
            t = abs(i - num_bars // 2) / (num_bars // 2)
            bar.set_fill(
                interpolate_color(
                    ManimColor(eq_color_left), ManimColor(eq_color_right), t
                ),
                opacity=0.9,
            )
            bar.set_stroke(width=0)
            bar.move_to(np.array([x, 0, 0]))
            bars.add(bar)

        self.add(bars)

        # Animate bars growing to random heights (podcast eq feel)
        random.seed(42)
        target_heights_list = [
            [0.3 + random.random() * 1.8 for _ in range(num_bars)] for _ in range(4)
        ]

        # Initial grow-in
        self.play(
            LaggedStart(
                *[
                    bar.animate.stretch_to_fit_height(target_heights_list[0][i]).move_to(
                        bar.get_center()
                    )
                    for i, bar in enumerate(bars)
                ],
                lag_ratio=0.03,
            ),
            run_time=0.6,
        )

        # Pulse the EQ bars a few times
        for cycle in range(1, 4):
            self.play(
                *[
                    bar.animate.stretch_to_fit_height(
                        target_heights_list[cycle][i]
                    ).move_to(bar.get_center())
                    for i, bar in enumerate(bars)
                ],
                run_time=0.3,
            )

        # ── PHASE 2: Ring sweeps in, bars shrink away ──
        ring = Circle(radius=2.5)
        ring.set_stroke("#3E5F33", width=5, opacity=0)
        ring.set_fill(opacity=0)

        self.play(
            *[
                bar.animate.stretch_to_fit_height(0.05).set_opacity(0)
                for bar in bars
            ],
            ring.animate.set_stroke(opacity=1),
            Create(ring),
            run_time=1.0,
        )
        self.remove(bars)

        # Ring glow pulse
        ring_glow = ring.copy().set_stroke("#56723E", width=14, opacity=0.3)
        self.play(
            FadeIn(ring_glow, scale=0.97),
            run_time=0.5,
        )
        self.play(
            ring_glow.animate.scale(1.06).set_stroke(opacity=0),
            run_time=0.6,
        )
        self.remove(ring_glow)

        # ── PHASE 3: Mic icon fades in at center ──
        mic_head = RoundedRectangle(
            width=0.6,
            height=0.9,
            corner_radius=0.28,
        ).set_fill("#6B4528", opacity=1).set_stroke("#8B6238", width=2)

        mic_arc = Arc(
            radius=0.5,
            start_angle=PI + PI / 6,
            angle=-PI - PI / 3,
        ).set_stroke("#6B4528", width=4)
        mic_arc.next_to(mic_head, DOWN, buff=-0.15)

        mic_stem = Line(ORIGIN, DOWN * 0.5).set_stroke("#6B4528", width=5)
        mic_stem.next_to(mic_arc, DOWN, buff=-0.02)

        mic_base = Line(LEFT * 0.35, RIGHT * 0.35).set_stroke("#6B4528", width=5)
        mic_base.next_to(mic_stem, DOWN, buff=0)

        mic = VGroup(mic_head, mic_arc, mic_stem, mic_base)
        mic.move_to(UP * 0.3)

        # Sound wave arcs emanating from mic
        wave_left = VGroup()
        wave_right = VGroup()
        for j in range(3):
            arc_l = Arc(
                radius=0.8 + j * 0.35,
                start_angle=PI / 2 + PI / 6,
                angle=PI / 3,
            ).set_stroke("#56723E", width=3 - j * 0.6, opacity=0.7 - j * 0.15)
            arc_l.move_to(mic_head.get_center() + LEFT * 0.3)
            wave_left.add(arc_l)

            arc_r = Arc(
                radius=0.8 + j * 0.35,
                start_angle=PI / 2 - PI / 6,
                angle=-PI / 3,
            ).set_stroke("#56723E", width=3 - j * 0.6, opacity=0.7 - j * 0.15)
            arc_r.move_to(mic_head.get_center() + RIGHT * 0.3)
            wave_right.add(arc_r)

        self.play(FadeIn(mic, scale=0.7), run_time=0.8)
        self.play(
            LaggedStart(
                *[Create(a) for a in wave_left],
                *[Create(a) for a in wave_right],
                lag_ratio=0.12,
            ),
            run_time=0.8,
        )

        # Pulse mic and waves
        self.play(
            mic.animate.scale(1.08),
            wave_left.animate.scale(1.1).set_opacity(0.9),
            wave_right.animate.scale(1.1).set_opacity(0.9),
            run_time=0.25,
        )
        self.play(
            mic.animate.scale(1 / 1.08),
            wave_left.animate.scale(1 / 1.1).set_opacity(0.6),
            wave_right.animate.scale(1 / 1.1).set_opacity(0.6),
            run_time=0.25,
        )

        # ── PHASE 4: Text appears below ──
        subtitle = Text(
            "Cerita dari",
            font_size=36,
            slant=ITALIC,
            color="#8B6238",
        )
        title = Text(
            "NGADIPRONO",
            font_size=60,
            weight=BOLD,
            color="#6B4528",
        )
        text_group = VGroup(subtitle, title).arrange(DOWN, buff=0.1)
        text_group.next_to(ring, DOWN, buff=0.35)

        # Underline flourish
        underline = Line(LEFT * 1.8, RIGHT * 1.8).set_stroke("#3E5F33", width=3)
        underline.next_to(title, DOWN, buff=0.15)

        self.play(
            FadeIn(subtitle, shift=UP * 0.2),
            run_time=0.7,
        )
        self.play(
            FadeIn(title, shift=UP * 0.2),
            GrowFromCenter(underline),
            run_time=0.8,
        )

        self.wait(0.5)

        # ── PHASE 5: Everything transitions to the actual logo ──
        logo = ImageMobject("assets/logo_arbe.png")
        logo.scale_to_fit_width(8)
        logo.set_opacity(0)
        self.add(logo)

        self.play(
            FadeOut(ring),
            FadeOut(mic),
            FadeOut(wave_left),
            FadeOut(wave_right),
            FadeOut(subtitle),
            FadeOut(title),
            FadeOut(underline),
            logo.animate.set_opacity(1),
            run_time=1.2,
        )

        # Breathing effect on logo
        self.play(logo.animate.scale(1.03), run_time=0.8, rate_func=there_and_back)

        self.wait(1.5)

        # Fade out
        self.play(FadeOut(logo), run_time=1.0)
