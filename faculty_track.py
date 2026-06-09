from manim import *


class FacultyEngineeringTrack(Scene):
    def construct(self):
        # =========================
        # CONFIG
        # =========================
        MAP_IMAGE = "assets/ft_track_map.png"

        # 16:9 scene
        self.camera.background_color = WHITE

        # =========================
        # BACKGROUND MAP
        # =========================
        map_img = ImageMobject(MAP_IMAGE)
        map_img.set_width(config.frame_width)
        self.add(map_img)

        # Manim scene coordinates:
        # x: left negative, right positive
        # y: bottom negative, top positive
        # Map reference (from image):
        #   Jl. Grafika = bottom-right area (~x=3.5, y=-2.2)
        #   Jl. Selokan Mataram = top (~y=3.0)
        #   Left boundary (near river) = ~x=-6.0
        #   Right boundary = ~x=6.5

        # =========================
        # MAIN BLUE TRACK ROUTE
        # Start: South end of Jl. Grafika (near Jl. Sains)
        # Direction: north from start → L-turn through campus roads
        #   → east to join right perimeter → north up right side
        #   → west across top → south down left side
        #   → east across bottom → return to start
        # =========================
        route_points = [
            # === START: South end of Jl. Grafika, near Jl. Sains ===
            [2.5, -3.0, 0],

            # Go NORTH up Jl. Grafika road
            [2.5, -2.6, 0],
            [2.4, -2.2, 0],

            # Tight LEFT turn (west) at intersection — from zoomed images
            [2.2, -2.0, 0],
            [1.8, -1.85, 0],
            [1.3, -1.8, 0],

            # Tight turn back NORTH on next road
            [1.05, -1.6, 0],
            [0.9, -1.2, 0],
            [0.8, -0.6, 0],

            # Continue north, curving northeast
            [0.9, 0.0, 0],
            [1.3, 0.5, 0],
            [2.0, 0.8, 0],

            # Head east to join the eastern perimeter road
            [3.0, 1.0, 0],
            [4.0, 1.1, 0],
            [4.8, 1.3, 0],

            # Up the east side (heading north)
            [5.3, 1.7, 0],
            [5.6, 2.2, 0],

            # Top-right corner — tight turn west
            [5.5, 2.7, 0],
            [5.0, 2.95, 0],
            [4.2, 3.05, 0],

            # West along the top (Jl. Selokan Mataram)
            [3.0, 3.12, 0],
            [1.5, 3.18, 0],
            [0.0, 3.2, 0],
            [-1.5, 3.2, 0],
            [-3.0, 3.1, 0],
            [-3.8, 3.0, 0],

            # Down the left/west side (heading south, near river)
            [-4.5, 2.6, 0],
            [-5.0, 1.8, 0],
            [-5.3, 0.8, 0],
            [-5.6, -0.1, 0],
            [-6.1, -0.8, 0],
            [-6.35, -1.6, 0],

            # Bottom-left corner — tight turn east
            [-6.1, -2.1, 0],
            [-5.3, -2.4, 0],
            [-4.2, -2.6, 0],

            # East across the bottom road
            [-3.0, -2.75, 0],
            [-1.5, -2.85, 0],
            [0.0, -2.9, 0],
            [1.2, -2.95, 0],
            [2.0, -3.0, 0],

            # Return to START
            [2.5, -3.0, 0],
        ]

        route = VMobject()
        route.set_points_smoothly([np.array(p) for p in route_points])
        route.set_stroke(color=BLUE_D, width=12, opacity=0.95)

        # Glowing duplicate track
        route_glow = route.copy()
        route_glow.set_stroke(color=BLUE_A, width=22, opacity=0.35)

        # =========================
        # START MARKER
        # =========================
        start_dot = Dot(
            point=np.array(route_points[0]),
            radius=0.18,
            color=GREEN
        )
        start_dot.set_stroke(BLACK, width=3)

        start_label = Text("START", font_size=28, weight=BOLD, color=GREEN)
        start_label.set_stroke(BLACK, width=4, opacity=0.8)
        start_label.next_to(start_dot, DOWN, buff=0.15)

        start_sublabel = Text(
            "Jl. Grafika", font_size=22, color=GREEN_D
        )
        start_sublabel.set_stroke(BLACK, width=3, opacity=0.6)
        start_sublabel.next_to(start_label, DOWN, buff=0.08)

        start_group = VGroup(start_dot, start_label, start_sublabel)

        # =========================
        # MOVING RUNNER
        # =========================
        runner = Dot(radius=0.14, color=YELLOW)
        runner.set_stroke(BLACK, width=3)
        runner.move_to(route_points[0])

        runner_trail = TracedPath(
            runner.get_center,
            stroke_color=YELLOW,
            stroke_width=4,
            stroke_opacity=0.6,
        )

        # =========================
        # DIRECTION ARROWS along route
        # =========================
        arrow_indices = [3, 8, 13, 19, 23, 28]
        direction_arrows = VGroup()
        for i in arrow_indices:
            if i + 1 < len(route_points):
                start_pt = np.array(route_points[i])
                end_pt = np.array(route_points[i + 1])
                direction = end_pt - start_pt
                direction = direction / np.linalg.norm(direction) * 0.4
                arrow = Arrow(
                    start_pt - direction * 0.5,
                    start_pt + direction * 0.5,
                    buff=0,
                    stroke_width=6,
                    max_tip_length_to_length_ratio=0.4,
                    color=BLUE_B,
                )
                arrow.set_opacity(0.7)
                direction_arrows.add(arrow)

        # =========================
        # TITLE / INSTRUCTION TEXT
        # =========================
        title = Text(
            "Faculty of Engineering Track",
            font_size=38,
            weight=BOLD,
            color=BLACK
        )
        title.set_stroke(WHITE, width=6, opacity=0.8, background=True)
        title.to_edge(UP)

        subtitle = Text(
            "Starting from Jl. Grafika",
            font_size=26,
            color=DARK_GRAY
        )
        subtitle.set_stroke(WHITE, width=5, opacity=0.8, background=True)
        subtitle.next_to(title, DOWN, buff=0.15)

        # =========================
        # ANIMATION
        # =========================

        # Show title
        self.play(FadeIn(title), FadeIn(subtitle), run_time=1)
        self.wait(0.5)

        # Show start marker
        self.play(FadeIn(start_group), run_time=0.8)
        self.play(Indicate(start_dot, color=GREEN, scale_factor=1.5), run_time=0.6)
        self.wait(0.5)

        # Draw the full route
        self.play(Create(route_glow), Create(route), run_time=5)
        self.wait(0.3)

        # Show direction arrows
        self.play(
            LaggedStart(
                *[FadeIn(a, scale=0.5) for a in direction_arrows],
                lag_ratio=0.15
            ),
            run_time=1.5
        )
        self.wait(0.3)

        # Show runner and traced path
        self.add(runner_trail)
        self.play(FadeIn(runner), run_time=0.3)

        # Move runner along the full route
        self.play(
            MoveAlongPath(runner, route),
            run_time=14,
            rate_func=linear
        )

        self.wait(0.5)

        # Finish label
        finish_label = Text(
            "FINISH", font_size=28, weight=BOLD, color=RED_D
        )
        finish_label.set_stroke(BLACK, width=4, opacity=0.8)
        finish_label.next_to(runner, UP, buff=0.15)
        self.play(FadeIn(finish_label), run_time=0.5)

        # Final summary
        summary = Text(
            "Loop complete — back to Jl. Grafika",
            font_size=30,
            weight=BOLD,
            color=BLUE_D,
        )
        summary.set_stroke(WHITE, width=6, opacity=0.9, background=True)
        summary.to_edge(DOWN)

        self.play(FadeIn(summary), run_time=0.8)
        self.wait(2)