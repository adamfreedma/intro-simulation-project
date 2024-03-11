import customtkinter as ctk
from start_frame import StartFrame
from config_choose_frame import ConfigChooseFrame
from simulation import Simulation
from walker import Walker
from typing import List
import threading
from straight_walker import StraightWalker


class MainFrame(ctk.CTkFrame):

    def __init__(self, master, simulation: Simulation):
        ctk.CTkFrame.__init__(self, master, corner_radius=15)

        self.height = master.height
        self.width = master.width

        self.simulation = simulation
        self.walkers: List[Walker] = [
            StraightWalker(True),
            StraightWalker(True),
            StraightWalker(True),
        ]

        self.start_frame = StartFrame(self)
        self.config_choose_frame = ConfigChooseFrame(self)
        self.padding = 30

        # layout
        self.config_choose_frame.pack(anchor="s", pady=self.padding)
        self.start_frame.pack(anchor="s", pady=self.padding)

    def start_simulation(self, visual: bool):
        if visual:
            visual_thread = threading.Thread(target=self.simulation.run_visual)
            visual_thread.start()

        for walker in self.walkers:
            print(walker)
            walker_thread = threading.Thread(
                target=self.simulation.simulate, args=[walker]
            )
            walker_thread.start()

    def parse_teleporters_config(self, path: str) -> bool:
        return self.simulation.config_teleporters(path)

    def parse_obstacles_config(self, path: str) -> bool:
        return self.simulation.config_obstacles(path)
