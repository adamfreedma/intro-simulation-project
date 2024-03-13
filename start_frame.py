import customtkinter as ctk
import colors
from spinbox import Spinbox


class StartFrame(ctk.CTkFrame):

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master, corner_radius=15)

        self.height = master.height
        self.width = master.width
        self.widget_width = self.width // 8
        self.padding = master.padding

        self.visual_var = ctk.BooleanVar(self, value=False)
        self.progress_var = ctk.DoubleVar(self, value=0)

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
        
        self.progress_bar = ctk.CTkProgressBar(self,
            self.widget_width * 2,
            corner_radius=5,
            variable=self.progress_var,
        )

        self.graph_output_folder_widget = ctk.CTkEntry(self, self.widget_width * 2, placeholder_text="Graph output file:",corner_radius=5)

        self.simulation_count_widget = Spinbox(self, width=self.widget_width, starting_value=500, text="Simulation count")
        self.max_steps_widget = Spinbox(self, width=self.widget_width, starting_value=100, text="Max steps")


        # layout
        self.graph_output_folder_widget.grid(row=0, column=3, padx=self.padding, pady=self.padding)
        self.max_steps_widget.grid(row=0, column=2, padx=self.padding, pady=self.padding)
        self.simulation_count_widget.grid(row=0, column=1, padx=self.padding, pady=self.padding)
        self.visual_toggle.grid(row=0, column=0, padx=self.padding, pady=self.padding)
        self.start_button.grid(row=1, column=1, padx=self.padding, pady=self.padding)

    def start(self):
        self.progress_bar.grid(row=2, column=1, padx=self.padding, pady=self.padding)
        self.master.start_simulation(self.visual_var.get(),
                                     self.progress_var,
                                     simulation_count=self.simulation_count_widget.get(),
                                     max_steps=self.max_steps_widget.get(),
                                     graph_output_folder=self.graph_output_folder_widget.get(),
                                    )
