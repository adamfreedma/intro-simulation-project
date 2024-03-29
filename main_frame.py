import customtkinter as ctk # type: ignore[import]
from customtkinter import DoubleVar
from start_frame import StartFrame
from config_choose_frame import ConfigChooseFrame
from walker_config_frame import WalkerConfigFrame
from simulation import Simulation
import threading
from straight_walker import StraightWalker
import os
import shutil
from typing import List
from typing import Optional

class MainFrame(ctk.CTkFrame): # type: ignore[misc]
    
    __FOLDER_PREFIX = "GRAPHS"
    
    def __init__(self, tab_master: ctk.CTkFrame, master: ctk.CTkFrame, simulation: Simulation) -> None:
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

    def get_folder_prefix(self) -> str:
        return self.__FOLDER_PREFIX

    def start_simulation(self, visual: bool, progress_var: DoubleVar,
                         simulation_count: Optional[int]=None,
                         max_steps: Optional[int]=None,
                         graph_output_folder: str="") -> None:
        
        self.stop_event.clear()

        if graph_output_folder:
            graph_output_folder = self.__FOLDER_PREFIX + graph_output_folder

            if os.path.isdir(graph_output_folder):
                shutil.rmtree(graph_output_folder)

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
        walker_list = self.walker_config_frame.get_walkers()
        run_event_dict = {walker : threading.Event() for walker in walker_list}

        for walker in walker_list:
            output_path = None
            if graph_output_folder:
                output_path = f"{graph_output_folder}/{walker.get_name()}"
            
            walker_thread = threading.Thread(
                target=self.simulation.simulate,
                args=[walker, self.stop_event, run_event_dict, progress_var, walker_list, visual, output_path]
            )
            walker_thread.start()
            
            walker_thread_list.append(walker_thread)
            
        self.wait_to_stop(walker_thread_list)
            
    def wait_to_stop(self, walker_thread_list: List[threading.Thread]) -> None:
        if all([not walker_thread.is_alive() for walker_thread in walker_thread_list]):
            self.simulation.stop()
            self.start_frame.stop()
        else:
            self.after(50, self.wait_to_stop, walker_thread_list)

    def update_speed(self, value: float) -> None:
        self.simulation.update_speed(value)
        
    def update_simulation_count(self, value: int) -> None:
        self.simulation.set_simulation_count(value)
        
    def get_simulation_count(self) -> int:
        return self.simulation.get_simulation_count()
        
    def update_max_steps(self, value: int) -> None:
        self.simulation.set_max_steps(value)
        
    def get_max_steps(self) -> int:
        return self.simulation.get_max_steps()

    def parse_config(self, path: str) -> bool:
        return self.simulation.config(path)