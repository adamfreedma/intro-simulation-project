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
        
        self.horizontal_frame = ctk.CTkFrame(self)

        self.progress_bar = ctk.CTkProgressBar(
            self,
            self.widget_width * 2,
            corner_radius=5,
            variable=self.progress_var,
        )

        self.start_button = ctk.CTkButton(
            self,
            self.widget_width,
            text="Start!",
            command=self.start,
            fg_color=colors.RED,
        )
        
        self.speed_slider_frame = ctk.CTkFrame(self.horizontal_frame)
        self.speed_slider = ctk.CTkSlider(
            self.speed_slider_frame,
            self.widget_width,
            command=self.update_speed
        )
        self.speed_slider.set(1)
        self.speed_slider_title = ctk.CTkLabel(
            self.speed_slider_frame,
            text="Visual simulation speed:"
        )
        
        self.visual_toggle = ctk.CTkSwitch(
            self.horizontal_frame,
            self.widget_width,
            text=":Visual",
            variable=self.visual_var,
            onvalue=True,
            offvalue=False,
            button_color=colors.WHITE,
        )

        self.graph_output_folder_widget = ctk.CTkEntry(
            self.horizontal_frame,
            self.widget_width,
            placeholder_text="Graphs folder:",
            corner_radius=5,
        )

        self.simulation_count_widget = Spinbox(
            self.horizontal_frame,
            width=self.widget_width,
            starting_value=500,
            text="Simulation count",
            command=self.update_simulation_count,
        )
        self.max_steps_widget = Spinbox(
            self.horizontal_frame,
            width=self.widget_width,
            starting_value=100,
            text="Max steps",
            command=self.update_max_steps,
        )


        # layout
        self.speed_slider_title.pack(expand=True, padx=self.padding, pady=self.padding)
        self.speed_slider.pack(expand=True, padx=self.padding, pady=self.padding)
        
        self.graph_output_folder_widget.pack(side="right", expand=True, padx=self.padding, pady=self.padding)
        self.max_steps_widget.pack(side="right", expand=True, padx=self.padding, pady=self.padding)
        self.speed_slider_frame.pack(side="right", expand=True, padx=self.padding, pady=self.padding)
        self.simulation_count_widget.pack(side="right", expand=True, padx=self.padding, pady=self.padding)
        self.visual_toggle.pack(side="right", expand=True, padx=self.padding, pady=self.padding)
        self.horizontal_frame.pack(expand=True, padx=self.padding, pady=self.padding)
        
        self.start_button.pack(expand=True, padx=self.padding, pady=self.padding)

    def start(self):
        self.progress_bar.pack(expand=True, padx=self.padding, pady=self.padding)
        self.master.start_simulation(self.visual_var.get(),
                                     self.progress_var,
                                     simulation_count=self.simulation_count_widget.get(),
                                     max_steps=self.max_steps_widget.get(),
                                     graph_output_folder=self.graph_output_folder_widget.get(),
                                    )

    def update_speed(self, value: float):
        self.master.update_speed(value)

    def update_simulation_count(self, value: int):
        self.master.update_simulation_count(value)
        
    def update_max_steps(self, value: int):
        self.master.update_max_steps(value)

    def stop(self):
        self.progress_bar.pack_forget()