from manim import *

# Set scene resolution and aspect ratio to match the map image (868x798)
config.pixel_width = 868
config.pixel_height = 798
config.frame_width = 14.2222222
config.frame_height = 14.2222222 * 798 / 868


class ExitRoutes(Scene):
    def construct(self):
        # =========================
        # CONFIG
        # =========================
        MAP_IMAGE = "assets/ft_track_map.png"

        # Set to True to overlay a labeled coordinate grid for editing positions.
        # Set to False to run the actual final animation.
        SHOW_COORDINATE_GRID = False

        self.camera.background_color = WHITE

        # =========================
        # BACKGROUND MAP
        # =========================
        map_img = ImageMobject(MAP_IMAGE)
        map_img.set_width(config.frame_width)
        self.add(map_img)

        # =========================
        # TRACK ROUTE (thin reference line from faculty_track.py)
        # =========================
        route_points = [
            [4.3, -2.8, 0],
            [4.15, -1.9, 0],
            [4.1, -1.6, 0],
            [4.4, -0.5, 0],
            [5.0, 1.0, 0],
            [5.25, 2.0, 0],
            [5.0, 2.5, 0],
            [3.5, 3.0, 0],
            [2.5, 3.5, 0],
            [1.5, 3.9, 0],
            [0.5, 4.5, 0],
            [-0.5, 5, 0],
            [-1.5, 4.8, 0],
            [-2.75, 4.65, 0],
            [-3.25, 4.3, 0],
            [-3.65, 3.5, 0],
            [-3.65, 2.5, 0],
            [-3.6, 2.0, 0],
            [-3.48, 1.0, 0],
            [-4.25, 0.0, 0],
            [-4.85, -0.25, 0],
            [-6.15, -1.0, 0],
            [-6.60, -1.5, 0],
            [-6.75, -2.0, 0],
            [-6.75, -2.5, 0],
            [-6.65, -3.0, 0],
            [-6.0, -3.5, 0],
            [-5.0, -3.9, 0],
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
            [4.3, -2.8, 0],
        ]

        # =========================
        # EXIT POINT DEFINITIONS
        # =========================

        # NOT ALLOWED exits (red X)
        blocked_exits = [
            {
                "pos": [5.5, 2.3, 0],       # Top-right, near Jl. Teknik intersection
                "label": "Jl. Teknik",
                "label_dir": LEFT,
            },
        ]

        # ALLOWED exits (green checkmark)
        allowed_exits = [
            {
                "pos": [4.3, -2.8, 0],      # START point — Jl. Grafika
                "label": "Jl. Grafika\n(Start/Finish)",
                "label_dir": LEFT,
            },
            {
                "pos": [4.5, -5.75, 0],     # Bottom-right gate to bigger road
                "label": "Gerbang Selatan\n(Jl. Kesehatan)",
                "label_dir": LEFT,
            },
        ]

        # =========================
        # COORDINATE GRID HELPER (for editing)
        # =========================
        if SHOW_COORDINATE_GRID:
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

            origin_lbl = Text("0", font_size=14, color=RED)
            origin_lbl.set_stroke(WHITE, width=3, background=True)
            origin_lbl.move_to([-0.25, -0.25, 0])
            self.add(origin_lbl)

            # Show track route
            trace_line = VMobject()
            trace_line.set_points_as_corners([np.array(p) for p in route_points])
            trace_line.set_stroke(color=BLUE_D, width=4, opacity=0.7)
            self.add(trace_line)

            # Show exit point dots with labels
            for i, ex in enumerate(blocked_exits):
                dot = Dot(ex["pos"], color=RED, radius=0.12)
                lbl = Text(f"BLOCKED {i}: [{ex['pos'][0]}, {ex['pos'][1]}]", font_size=12, color=RED)
                lbl.set_stroke(WHITE, width=3, background=True)
                lbl.next_to(dot, UR, buff=0.04)
                self.add(dot, lbl)

            for i, ex in enumerate(allowed_exits):
                dot = Dot(ex["pos"], color=GREEN, radius=0.12)
                lbl = Text(f"ALLOWED {i}: [{ex['pos'][0]}, {ex['pos'][1]}]", font_size=12, color=GREEN_E)
                lbl.set_stroke(WHITE, width=3, background=True)
                lbl.next_to(dot, UR, buff=0.04)
                self.add(dot, lbl)

            banner = Text("GRID MODE (Set SHOW_COORDINATE_GRID = False for final render)", font_size=16, color=RED)
            banner.set_stroke(WHITE, width=4, background=True)
            banner.to_edge(UP, buff=0.2)
            self.add(banner)

            self.wait(1)
            return

        # =========================
        # ANIMATION
        # =========================

        # --- Title ---
        title = Text(
            "Jalur Keluar / Exit Routes",
            font_size=36,
            weight=BOLD,
            color=BLACK
        )
        title.set_stroke(WHITE, width=6, opacity=0.8, background=True)
        title.to_edge(UP, buff=0.3)

        self.play(FadeIn(title), run_time=0.8)
        self.wait(0.5)

        # --- Draw thin reference track ---
        route_line = VMobject()
        route_line.set_points_as_corners([np.array(p) for p in route_points])
        route_line.set_stroke(color=BLUE_D, width=6, opacity=0.6)

        route_glow = route_line.copy()
        route_glow.set_stroke(color=BLUE_A, width=14, opacity=0.2)

        self.play(Create(route_glow), Create(route_line), run_time=3)
        self.wait(0.5)

        # --- Show NOT ALLOWED exits ---
        not_allowed_header = Text(
            "❌ TIDAK BOLEH KELUAR",
            font_size=28,
            weight=BOLD,
            color=RED,
        )
        not_allowed_header.set_stroke(WHITE, width=5, opacity=0.9, background=True)
        not_allowed_header.to_edge(UP, buff=0.3)

        self.play(FadeOut(title), FadeIn(not_allowed_header), run_time=0.6)

        for ex in blocked_exits:
            pos = np.array(ex["pos"])

            # Draw a big red X
            x_size = 0.5
            line1 = Line(
                pos + np.array([-x_size, x_size, 0]),
                pos + np.array([x_size, -x_size, 0]),
                stroke_width=10,
                color=RED,
            )
            line2 = Line(
                pos + np.array([-x_size, -x_size, 0]),
                pos + np.array([x_size, x_size, 0]),
                stroke_width=10,
                color=RED,
            )
            x_mark = VGroup(line1, line2)

            # Red glow circle behind X
            glow_circle = Circle(
                radius=0.7,
                stroke_width=4,
                stroke_color=RED,
                fill_color=RED,
                fill_opacity=0.15,
            )
            glow_circle.move_to(pos)

            # Label
            label = Text(
                ex["label"],
                font_size=22,
                weight=BOLD,
                color=RED,
            )
            label.set_stroke(WHITE, width=4, opacity=0.9, background=True)
            label.next_to(glow_circle, ex["label_dir"], buff=0.2)

            self.play(
                GrowFromCenter(glow_circle),
                run_time=0.5,
            )
            self.play(
                Create(line1),
                Create(line2),
                run_time=0.5,
            )
            self.play(FadeIn(label, shift=DOWN * 0.2), run_time=0.4)

        self.wait(1)

        # --- Show ALLOWED exits ---
        allowed_header = Text(
            "✅ BOLEH KELUAR",
            font_size=28,
            weight=BOLD,
            color=GREEN_D,
        )
        allowed_header.set_stroke(WHITE, width=5, opacity=0.9, background=True)
        allowed_header.to_edge(UP, buff=0.3)

        self.play(FadeOut(not_allowed_header), FadeIn(allowed_header), run_time=0.6)

        for ex in allowed_exits:
            pos = np.array(ex["pos"])

            # Green circle marker
            marker_circle = Circle(
                radius=0.5,
                stroke_width=4,
                stroke_color=GREEN,
                fill_color=GREEN,
                fill_opacity=0.2,
            )
            marker_circle.move_to(pos)

            # Checkmark (V shape)
            check = VMobject()
            check.set_points_as_corners([
                pos + np.array([-0.25, 0.0, 0]),
                pos + np.array([-0.05, -0.2, 0]),
                pos + np.array([0.25, 0.25, 0]),
            ])
            check.set_stroke(color=GREEN, width=8)

            # Label
            label = Text(
                ex["label"],
                font_size=20,
                weight=BOLD,
                color=GREEN_E,
            )
            label.set_stroke(WHITE, width=4, opacity=0.9, background=True)
            label.next_to(marker_circle, ex["label_dir"], buff=0.2)

            self.play(
                GrowFromCenter(marker_circle),
                run_time=0.5,
            )
            self.play(
                Create(check),
                run_time=0.4,
            )
            self.play(FadeIn(label, shift=DOWN * 0.2), run_time=0.4)

        self.wait(1)

        # --- Final summary ---
        summary = Text(
            "Keluar hanya melalui jalur yang ditentukan!",
            font_size=26,
            weight=BOLD,
            color=BLUE_D,
        )
        summary.set_stroke(WHITE, width=6, opacity=0.9, background=True)
        summary.to_edge(DOWN, buff=0.4)

        self.play(FadeIn(summary), run_time=0.8)
        self.wait(2)
