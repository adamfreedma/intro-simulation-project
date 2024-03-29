import customtkinter as ctk # type: ignore[import]
import colors
from spinbox import Spinbox


class StartFrame(ctk.CTkFrame): # type: ignore[misc]

    def __init__(self, master: ctk.CTkFrame) -> None:
        """
        Initializes the StartFrame class.

        Args:
            master (ctk.CTkFrame): The master frame.

        Returns:
            None
        """
        ctk.CTkFrame.__init__(self, master, corner_radius=15)

        self.height = master.height
        self.width = master.width
        self.widget_width = self.width // 8
        self.padding = master.padding
        
        # initialize variables
        self.visual_var = ctk.BooleanVar(self, value=False)
        self.progress_var = ctk.DoubleVar(self, value=0)

        # initialize widgets
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

    def start(self) -> None:
        """
        Packs the progress bar widget and calls the `start_simulation` method of the master object
        with the selected options from the GUI.
        """
        self.progress_bar.pack(expand=True, padx=self.padding, pady=self.padding)
        self.master.start_simulation(self.visual_var.get(),
                                     self.progress_var,
                                     simulation_count=self.simulation_count_widget.get(),
                                     max_steps=self.max_steps_widget.get(),
                                     graph_output_folder=self.graph_output_folder_widget.get(),
                                    )

    def update_speed(self, value: float) -> None:
        """
        Updates the speed of the object.

        Args:
            value (float): The new speed value.
        """
        self.master.update_speed(value)
        
    def get_speed(self) -> float:
        """
        Get the current speed value.

        Returns:
            float: The current speed value.
        """
        return self.speed_slider.get()

    def update_simulation_count(self, value: int) -> None:
        """
        Updates the simulation count.

        Args:
            value (int): The new simulation count value.
        """
        self.master.update_simulation_count(value)
        
    def get_simulation_count(self) -> int:
        """
        Get the current simulation count value.

        Returns:
            int: The current simulation count value.
        """
        return self.master.get_simulation_count()
        
    def update_max_steps(self, value: int) -> None:
        """
        Updates the max steps.

        Args:
            value (int): The new max steps value.
        """
        self.master.update_max_steps(value)
        
    def get_max_steps(self) -> int:
        """
        Get the current max steps value.

        Returns:
            int: The current max steps value.
        """
        return self.master.get_max_steps()

    def stop(self) -> None:
        """
        Hides the progress bar.
        """
        self.progress_bar.pack_forget()