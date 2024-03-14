import customtkinter as ctk
from customtkinter import DoubleVar
from start_frame import StartFrame
from config_choose_frame import ConfigChooseFrame
from walker_config_frame import WalkerConfigFrame
from simulation import Simulation
import threading
from straight_walker import StraightWalker
import os
from typing import List

class MainFrame(ctk.CTkFrame):
    
    __FOLDER_PREFIX = "GRAPHS"
    
    def __init__(self, tab_master, master, simulation: Simulation):
        ctk.CTkFrame.__init__(self, tab_master, corner_radius=15)

        self.height = master.height
        self.width = master.width
        self.padding = master.padding
        self.main_master = master

        self.stop_event = threading.Event()
        self.simulation = simulation

        self.start_frame = StartFrame(self)
        self.config_choose_frame = ConfigChooseFrame(self)
        self.walker_config_frame = WalkerConfigFrame(self)

        # layout
        self.walker_config_frame.pack(anchor="s", fill="both", padx=self.padding, pady=self.padding)
        self.config_choose_frame.pack(anchor="s", fill="both", padx=self.padding, pady=self.padding)
        self.start_frame.pack(anchor="s", fill="both", padx=self.padding, pady=self.padding)

    def start_simulation(self, visual: bool, progress_var: DoubleVar,
                         simulation_count: int=None, max_steps: int=None, graph_output_folder: str=None):
        self.stop_event.clear()

        graph_output_folder = self.__FOLDER_PREFIX + graph_output_folder

        if graph_output_folder and not os.path.isdir(graph_output_folder):
            os.mkdir(graph_output_folder)

        if simulation_count:
            self.simulation.set_simulation_count(simulation_count)
        if max_steps:
            self.simulation.set_max_steps(max_steps)

        if visual:
            visual_thread = threading.Thread(
                target=self.simulation.run_visual, args=[self.stop_event]
            )
            visual_thread.start()

        walker_thread_list: List[threading.Thread] = []

        for walker in self.walker_config_frame.get_walkers():
            output_path = None
            if graph_output_folder:
                output_path = f"{graph_output_folder}\\{walker.get_name()}"
            
            walker_thread = threading.Thread(
                target=self.simulation.simulate,
                args=[walker, self.stop_event, progress_var, visual, output_path]
            )
            walker_thread.start()
            
            walker_thread_list.append(walker_thread)
            
        self.wait_to_stop(walker_thread_list)
            
    def wait_to_stop(self, walker_thread_list: List[threading.Thread]):
        if all([not walker_thread.is_alive() for walker_thread in walker_thread_list]):
            self.simulation.stop()
            self.start_frame.stop()
        else:
            self.after(50, self.wait_to_stop, walker_thread_list)

    def update_speed(self, value: float):
        self.simulation.update_speed(value)
        
    def update_simulation_count(self, value: int):
        self.simulation.set_simulation_count(value)
        
    def update_max_steps(self, value: int):
        self.simulation.set_max_steps(value)

    def parse_config(self, path: str) -> bool:
        return self.simulation.config(path)