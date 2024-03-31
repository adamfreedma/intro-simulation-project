import customtkinter as ctk # type: ignore[import]
from spinbox import Spinbox
import colors
from stock_walker import StockWalker
from walker import Walker
from straight_walker import StraightWalker
from random_angle_walker import RandomAngleWalker
from random_walker import RandomWalker
from biased_walker import BiasedWalker
from accelerating_walker import AcceleratingWalker
from typing import List

class WalkerFrame(ctk.CTkFrame): # type: ignore[misc]

    __WALKER_TYPES = ["Straight", "Random Angle", "Random", "Biased", "Accelerating", "Stocks"]

    def __init__(self, master: ctk.CTkFrame) -> None:
        """
        Initialize the WalkerFrame object.

        Args:
            master (ctk.CTkFrame): The master frame that contains the WalkerFrame.
        """
        ctk.CTkFrame.__init__(self, master, corner_radius=15)

        self.height = master.height
        self.width = master.width
        self.widget_width = self.width // 8
        self.padding = master.padding

        self.walker_list: List[Walker] = []

        self.walker_type = ctk.StringVar(self.master, value="Straight")
        self.dimension_var = ctk.BooleanVar(value=False)

        self.delete_button = ctk.CTkButton(self, 0, text="X", fg_color=colors.RED, command=self.delete)
        self.walker_choose_dropdown = ctk.CTkOptionMenu(
            self,
            self.widget_width,
            values=self.__WALKER_TYPES,
            variable=self.walker_type,
            command=self.pack_walker_specific_widgets
        )

        self.dimension_toggle = ctk.CTkSwitch(
            self,
            self.widget_width,
            text=":3D",
            variable=self.dimension_var,
            onvalue=True,
            offvalue=False,
            button_color=colors.WHITE,
        )

        self.mass_spinbox = Spinbox(
            self,
            width=self.widget_width,
            starting_value=1,
            text="Mass",
        )
        
        # biased walker specific widgets
        self.bias_entry_frame = ctk.CTkFrame(self, self.widget_width)
        self.bias_entry_text = ctk.CTkLabel(self.bias_entry_frame, 0, text="Bias type:")
        self.bias_entry = ctk.CTkOptionMenu(
            self.bias_entry_frame,
            self.widget_width,
            values=["Origin"] + list(BiasedWalker.BIAS_DICT.keys()),
        )

        self.bias_entry_text.pack(padx=self.padding, pady=self.padding)
        self.bias_entry.pack(padx=self.padding, pady=self.padding)

        # accelerating walker specific widgets
        self.acceleration_entry_frame = ctk.CTkFrame(self, self.widget_width)
        self.acceleration_entry_text = ctk.CTkLabel(self.acceleration_entry_frame, 0, text="Acceleration type:")
        self.acceleration_entry = ctk.CTkOptionMenu(
            self.acceleration_entry_frame,
            self.widget_width,
            values=list(AcceleratingWalker.ACCELERATION_TYPES.keys()),
        )
        self.acceleration_entry_text.pack(padx=self.padding, pady=self.padding)
        self.acceleration_entry.pack(padx=self.padding, pady=self.padding)

        # layout
        self.walker_choose_dropdown.pack(expand=True, side="left", padx=self.padding, pady=self.padding)
        self.dimension_toggle.pack(side="left", padx=self.padding, pady=self.padding)
        self.mass_spinbox.pack(side="left", padx=self.padding, pady=self.padding)
        self.delete_button.pack(expand=True, side="right", padx=self.padding, pady=self.padding)
        
    def get_walker(self, name: str) -> Walker:
        """
        Returns an instance of a Walker based on the selected walker type.

        Args:
            name (str): The name of the walker.

        Returns:
            Walker: An instance of the selected walker type.

        """
        if self.walker_type.get() == "Random Angle":
            return RandomAngleWalker(name, self.dimension_toggle.get(), self.mass_spinbox.get())
        if self.walker_type.get() == "Random":
            return RandomWalker(name, self.dimension_toggle.get(), self.mass_spinbox.get())
        if self.walker_type.get() == "Biased":
            return BiasedWalker(name, self.dimension_toggle.get(), self.mass_spinbox.get(), self.bias_entry.get())
        if self.walker_type.get() == "Accelerating":
            return AcceleratingWalker(name, self.dimension_toggle.get(), self.mass_spinbox.get(), self.acceleration_entry.get())
        if self.walker_type.get() == "Stocks":
            return StockWalker(name, self.mass_spinbox.get())
        # defaults to Straight
        return StraightWalker(name, self.dimension_toggle.get(), self.mass_spinbox.get())
    
    def pack_walker_specific_widgets(self, current_value: str) -> None:
        """
        Packs the specific widgets based on the current value.

        Args:
            current_value (str): The current walker type to determine which widgets to pack.
        """
        if current_value == "Biased":
            # pack the bias entry frame and forget the acceleration entry frame
            self.bias_entry_frame.pack(side="left", padx=self.padding, pady=self.padding)
            self.acceleration_entry_frame.pack_forget()
        elif current_value == "Accelerating":
            # pack the acceleration entry frame and forget the bias entry frame
            self.acceleration_entry_frame.pack(side="left", padx=self.padding, pady=self.padding)
            self.bias_entry_frame.pack_forget()
        else:
            # forget both the bias and acceleration entry frames
            self.bias_entry_frame.pack_forget()
            self.acceleration_entry_frame.pack_forget()
    
    def delete(self) -> None:
        """
        Deletes the walker from the master and removes it from the GUI.
        """
        self.master.delete_walker(self)
        self.pack_forget()
        self.destroy()
        del self
        
        
