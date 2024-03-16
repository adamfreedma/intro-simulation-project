import customtkinter as ctk
from spinbox import Spinbox
import colors
from walker import Walker
from straight_walker import StraightWalker
from random_angle_walker import RandomAngleWalker
from random_walker import RandomWalker
from biased_walker import BiasedWalker

class WalkerFrame(ctk.CTkFrame):

    __WALKER_TYPES = ["Straight", "Random Angle", "Random", "Biased"]

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master, corner_radius=15)

        self.height = master.height
        self.width = master.width
        self.widget_width = self.width // 8
        self.padding = master.padding


        self.walker_list = []
        
        self.walker_type = ctk.StringVar(self.master, value="Straight")
        self.dimension_var = ctk.BooleanVar(value=False)
        
        self.delete_button = ctk.CTkButton(self, 0, text="X", fg_color=colors.RED, command=self.delete)
        self.walker_choose_dropdown = ctk.CTkOptionMenu(self, self.widget_width, values=self.__WALKER_TYPES, variable=self.walker_type)
        
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
        
        # layout
        self.walker_choose_dropdown.pack(expand=True, side="left", padx=self.padding, pady=self.padding)
        self.dimension_toggle.pack(side="left", padx=self.padding, pady=self.padding)
        self.mass_spinbox.pack(side="left", padx=self.padding, pady=self.padding)
        self.delete_button.pack(expand=True, side="right", padx=self.padding, pady=self.padding)
        
    def get_walker(self, name: str) -> Walker:
        if self.walker_type.get() == "Straight":
            return StraightWalker(name, self.dimension_toggle.get(), self.mass_spinbox.get())
        if self.walker_type.get() == "Random Angle":
            return RandomAngleWalker(name, self.dimension_toggle.get(), self.mass_spinbox.get())
        if self.walker_type.get() == "Random":
            return RandomWalker(name, self.dimension_toggle.get(), self.mass_spinbox.get())
        if self.walker_type.get() == "Biased":
            return BiasedWalker(name, self.dimension_toggle.get(), self.mass_spinbox.get())
    
    def delete(self):
        self.master.delete_walker(self)
        self.pack_forget()
        del self
        
        
