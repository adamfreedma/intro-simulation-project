import customtkinter as ctk
import colors
from walker_frame import WalkerFrame
from typing import List
from walker import Walker

class WalkerConfigFrame(ctk.CTkFrame):

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master, corner_radius=15)

        self.height = master.height
        self.width = master.width
        self.widget_width = self.width // 8
        self.padding = master.padding


        self.walker_frame_list: List[WalkerFrame] = []
        
        self.add_walker_button = ctk.CTkButton(self, self.widget_width, text="Add walker", command=self.create_walker)
        
        # layout
        self.add_walker_button.pack(padx=self.padding, pady=self.padding)
        
    
    def create_walker(self):
        walker_frame = WalkerFrame(self)
        self.walker_frame_list.append(walker_frame)
        walker_frame.pack(padx=self.padding, pady=self.padding)
        
    def delete_walker(self, walker_frame: WalkerFrame):
        self.walker_frame_list.remove(walker_frame)
        
    def get_walkers(self) -> List[Walker]:
        return [frame.get_walker(str(num)) for num, frame in enumerate(self.walker_frame_list)]
