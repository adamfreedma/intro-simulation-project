import customtkinter as ctk
import colors


class StartFrame(ctk.CTkFrame):

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master, corner_radius=15)

        self.height = master.height
        self.width = master.width
        self.widget_width = self.width // 8

        self.dimension_var = ctk.BooleanVar(value=False)

        self.dimension_toggle = ctk.CTkSwitch(
            self,
            self.widget_width,
            text=":3D",
            variable=self.dimension_var,
            onvalue=True,
            offvalue=False,
            button_color=colors.WHITE,
        )

        self.visual_var = ctk.BooleanVar(value=False)

        self.visual_toggle = ctk.CTkSwitch(
            self,
            self.widget_width,
            text=":Visual",
            variable=self.visual_var,
            onvalue=True,
            offvalue=False,
            button_color=colors.WHITE,
        )

        self.start_button = ctk.CTkButton(
            self,
            self.widget_width,
            text="Start!",
            command=self.start,
            fg_color=colors.RED,
        )

        # layout
        self.visual_toggle.pack(anchor="s")
        self.start_button.pack(anchor="s")

    def start(self):
        self.master.start_simulation(self.visual_var.get())
