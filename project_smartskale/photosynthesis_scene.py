from manim import *
 
class PhotosynthesisScene(Scene):
    def construct(self):
 
        # ─── 1. TITLE ───────────────────────────────────────────────────────────
        title = Text("Photosynthesis", font_size=48, color=GREEN_B)
        subtitle = Text("Class 10 Science | Chapter 6", font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)
 
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))
 
        # ─── 2. THE EQUATION ─────────────────────────────────────────────────────
        eq_label = Text("The Chemical Equation:", font_size=30, color=WHITE)
        eq_label.to_edge(UP, buff=0.6)
        self.play(Write(eq_label))
 
        equation = MathTex(
            r"6CO_2", r"+", r"6H_2O",
            r"\xrightarrow{\text{Sunlight + Chlorophyll}}",
            r"C_6H_{12}O_6", r"+", r"6O_2",
            font_size=48
        )
        equation.set_color_by_tex_to_color_map({
            r"6CO_2":        BLUE,
            r"6H_2O":        TEAL,
            r"C_6H_{12}O_6": YELLOW,
            r"6O_2":         GREEN,
        })
        equation.move_to(ORIGIN)
 
        # Animate each term appearing one by one
        for part in equation:
            self.play(FadeIn(part, shift=UP * 0.2), run_time=0.5)
        self.wait(0.8)
 
        # ─── 3. LABELS BELOW EACH TERM ───────────────────────────────────────────
        labels_data = [
            (equation[0], "Carbon\nDioxide",  BLUE),
            (equation[2], "Water",             TEAL),
            (equation[4], "Glucose",           YELLOW),
            (equation[6], "Oxygen",            GREEN),
        ]
 
        label_objects = []
        arrows = []
        for term, name, color in labels_data:
            lbl = Text(name, font_size=22, color=color)
            lbl.next_to(term, DOWN, buff=0.9)
            arr = Arrow(
                start=term.get_bottom() + DOWN * 0.05,
                end=lbl.get_top() + UP * 0.05,
                buff=0.1,
                color=color,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15
            )
            label_objects.append(lbl)
            arrows.append(arr)
 
        for arr, lbl in zip(arrows, label_objects):
            self.play(GrowArrow(arr), Write(lbl), run_time=0.6)
        self.wait(1.5)
 
        # ─── 4. HIGHLIGHT REACTANTS vs PRODUCTS ──────────────────────────────────
        reactant_box = SurroundingRectangle(
            VGroup(equation[0], equation[1], equation[2]),
            color=BLUE_C, buff=0.15, corner_radius=0.1
        )
        product_box = SurroundingRectangle(
            VGroup(equation[4], equation[5], equation[6]),
            color=GREEN_C, buff=0.15, corner_radius=0.1
        )
        reactant_text = Text("Reactants", font_size=20, color=BLUE_C)
        reactant_text.next_to(reactant_box, UP, buff=0.15)
        product_text = Text("Products", font_size=20, color=GREEN_C)
        product_text.next_to(product_box, UP, buff=0.15)
 
        self.play(
            Create(reactant_box), Write(reactant_text),
            Create(product_box),  Write(product_text),
            run_time=1
        )
        self.wait(2)
 
        # ─── 5. FADE OUT & SUMMARY CARD ──────────────────────────────────────────
        self.play(*[FadeOut(mob) for mob in self.mobjects])
 
        summary = VGroup(
            Text("Key Takeaway", font_size=36, color=YELLOW),
            Text("Plants absorb CO₂ + Water using Sunlight", font_size=26, color=WHITE),
            Text("→ to produce Glucose (food) + Oxygen", font_size=26, color=GREEN),
        ).arrange(DOWN, buff=0.4)
        summary.move_to(ORIGIN)
 
        for line in summary:
            self.play(FadeIn(line, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(2.5)
 
        self.play(FadeOut(summary))