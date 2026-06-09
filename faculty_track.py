from manim import *

# Set scene resolution and aspect ratio to match the map image (868x798) to prevent zooming/cropping
config.pixel_width = 868
config.pixel_height = 798
config.frame_width = 14.2222222
config.frame_height = 14.2222222 * 798 / 868


class FacultyEngineeringTrack(Scene):
    def construct(self):
        # =========================
        # CONFIG
        # =========================
        MAP_IMAGE = "assets/ft_track_map.png"

        # Set to True to overlay a labeled coordinate grid and show points with their indices.
        # Set to False to run the actual final animation.
        SHOW_COORDINATE_GRID = False

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
            [4.3, -2.8, 0],

            # Go NORTH up Jl. Grafika road to upper-right corner
            [4.15, -1.9, 0],
            [4.1, -1.6, 0],
            [4.4, -0.5, 0],
            [5.0, 1.0, 0],
            [5.25, 2.0, 0],

            # Top-right corner — curve west onto Jl. Selokan Mataram
            [5.0, 2.5, 0],
            
            # West along the top (Jl. Selokan Mataram)
            [3.5, 3.0, 0],
            [2.5, 3.5, 0],
            [1.5, 3.9, 0],
            [0.5, 4.5, 0],
            [-0.5, 5, 0],
            [-1.5, 4.8, 0],
            [-2.75, 4.65, 0],

            # Top-left corner — heading south
            [-3.25, 4.3, 0],
            [-3.65, 3.5, 0],

            # Down the left/west side (heading south, near river)
            [-3.65, 2.5, 0],
            [-3.6, 2.0, 0],
            [-3.48, 1.0, 0],
            [-4.25, 0.0, 0],
            [-4.85, -0.25, 0],
            [-6.15, -1.0, 0],

            # Bottom-left corner — tight turn east
            [-6.60, -1.5, 0],
            [-6.75, -2.0, 0],
            [-6.75, -2.5, 0],
            [-6.65, -3.0, 0],
            [-6.0, -3.5, 0],
            [-5.0, -3.9, 0],

            # East across the bottom road
            [-4.0, -4.1, 0],
            [-3.0, -3.75, 0],
            [-2.5, -3.5, 0],
            [-1.5, -3.25, 0],
            [-0.5, -3.6, 0],
            [0.5, -4.1, 0],
            [1.5, -4.7, 0],
            [2.5, -5.0, 0],
            [3.5, -5.4, 0],
            [4.45, -5.75, 0],
            [4.55, -5.1, 0],
            [4.4, -4.0, 0],

            # Return to START
            [4.3, -2.8, 0],
        ]

        # =========================
        # COORDINATE GRID HELPER (for editing)
        # =========================
        if SHOW_COORDINATE_GRID:
            # High-contrast coordinate grid (LaTeX-independent plane)
            grid = NumberPlane(
                x_range=[-8, 8, 1],
                y_range=[-8, 8, 1],
                background_line_style={
                    "stroke_color": RED,
                    "stroke_width": 1.5,
                    "stroke_opacity": 0.5
                },
                axis_config={
                    "stroke_color": RED,
                    "stroke_width": 3,
                }
            )
            self.add(grid)
            
            # Finer grid lines at 0.5 intervals
            fine_grid = NumberPlane(
                x_range=[-8, 8, 0.5],
                y_range=[-8, 8, 0.5],
                background_line_style={
                    "stroke_color": ORANGE,
                    "stroke_width": 0.8,
                    "stroke_opacity": 0.3
                }
            )
            self.add(fine_grid)

            # Manual text coordinate labels for axes (LaTeX-independent)
            for x in range(-7, 8):
                if x == 0:
                    continue
                lbl = Text(str(x), font_size=14, color=RED)
                lbl.set_stroke(WHITE, width=3, background=True)
                lbl.move_to([x, -0.3, 0])
                self.add(lbl)

            for y in range(-6, 7):
                if y == 0:
                    continue
                lbl = Text(str(y), font_size=14, color=RED)
                lbl.set_stroke(WHITE, width=3, background=True)
                lbl.move_to([-0.3, y, 0])
                self.add(lbl)

            # Origin label
            origin_lbl = Text("0", font_size=14, color=RED)
            origin_lbl.set_stroke(WHITE, width=3, background=True)
            origin_lbl.move_to([-0.25, -0.25, 0])
            self.add(origin_lbl)

            # Label all points with their indices and coordinates
            for idx, pt in enumerate(route_points):
                dot = Dot(pt, color=BLUE, radius=0.08)
                lbl_text = f"{idx}: [{pt[0]}, {pt[1]}]"
                lbl = Text(lbl_text, font_size=12, color=BLUE_E)
                lbl.set_stroke(WHITE, width=3, background=True)
                # Alternate label placement slightly to avoid overlap
                direction = UR if idx % 2 == 0 else DR
                lbl.next_to(dot, direction, buff=0.04)
                self.add(dot, lbl)

            # Add mode banner
            banner = Text("GRID MODE (Set SHOW_COORDINATE_GRID = False for final render)", font_size=16, color=RED)
            banner.set_stroke(WHITE, width=4, background=True)
            banner.to_edge(UP, buff=0.2)
            self.add(banner)
            
            # Trace lines
            trace_line = VMobject()
            trace_line.set_points_as_corners([np.array(p) for p in route_points])
            trace_line.set_stroke(color=BLUE_D, width=4, opacity=0.7)
            self.add(trace_line)

            self.wait(1)
            return

        route = VMobject()
        route.set_points_as_corners([np.array(p) for p in route_points])
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
        arrow_indices = [3, 9, 15, 22, 28, 35]
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