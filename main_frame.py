import customtkinter as ctk  # type: ignore[import]
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


class MainFrame(ctk.CTkFrame):  # type: ignore[misc]

    __FOLDER_PREFIX = "GRAPHS"

    def __init__(
        self, tab_master: ctk.CTkFrame, master: ctk.CTkFrame, simulation: Simulation
    ) -> None:
        """
        Initializes the MainFrame object.

        Args:
            tab_master (ctk.CTkFrame): The tab master frame.
            master (MainApp): The main app.
            simulation (Simulation): The simulation object.

        Returns:
            None
        """
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
        self.walker_config_frame.pack(
            anchor="s", fill="both", padx=self.padding, pady=self.padding
        )
        self.config_choose_frame.pack(
            anchor="s", fill="both", padx=self.padding, pady=self.padding
        )
        self.start_frame.pack(
            anchor="s", fill="both", padx=self.padding, pady=self.padding
        )

    def get_folder_prefix(self) -> str:
        """
        Returns the folder prefix used by the main frame.

        Returns:
            str: The folder prefix.
        """
        return self.__FOLDER_PREFIX

    def start_simulation(
        self,
        visual: bool,
        progress_var: DoubleVar,
        simulation_count: Optional[int] = None,
        max_steps: Optional[int] = None,
        graph_output_folder: str = "",
    ) -> None:
        """
        Starts the simulation.

        Args:
            visual (bool): Flag indicating whether to run the simulation in visual mode.
            progress_var (DoubleVar): Variable used to update the progress of the simulation.
            simulation_count (Optional[int], optional): Number of simulations to run. Defaults to None, which keeps the last amount.
            max_steps (Optional[int], optional): Maximum number of steps for each simulation. Defaults to None, which keeps the last amount.
            graph_output_folder (str, optional): Folder path to save the output graphs. Defaults to "".
        """
        self.stop_event.clear()

        if graph_output_folder:
            # adding the folder prefix to the output folder
            graph_output_folder = self.__FOLDER_PREFIX + graph_output_folder
            # clearing the folder if it already exists
            if os.path.isdir(graph_output_folder):
                shutil.rmtree(graph_output_folder)
            # making the folder
            os.mkdir(graph_output_folder)
        # setting the simulation count and max steps if they are provided
        if simulation_count:
            self.simulation.set_simulation_count(simulation_count)
        if max_steps:
            self.simulation.set_max_steps(max_steps)
        # starting the screen
        if visual:
            visual_thread = threading.Thread(
                target=self.simulation.run_visual, args=[self.stop_event]
            )
            visual_thread.start()
        # getting the events to detect when each walker is done
        walker_thread_list: List[threading.Thread] = []
        walker_list = self.walker_config_frame.get_walkers()
        run_event_dict = {walker: threading.Event() for walker in walker_list}
        # starting the simulation for each walker
        for walker in walker_list:
            output_path = None
            if graph_output_folder:
                output_path = f"{graph_output_folder}/{walker.get_name()}"

            walker_thread = threading.Thread(
                target=self.simulation.simulate,
                args=[
                    walker,
                    self.stop_event,
                    run_event_dict,
                    progress_var,
                    walker_list,
                    visual,
                    output_path,
                ],
            )
            walker_thread.start()

            walker_thread_list.append(walker_thread)
        # waiting for all walkers to finish
        self.wait_to_stop(walker_thread_list)

    def wait_to_stop(self, walker_thread_list: List[threading.Thread]) -> None:
        """
        Waits for all walker threads to stop before stopping the simulation and the start frame.

        Args:
            walker_thread_list (List[threading.Thread]): A list of walker threads.

        Returns:
            None
        """
        if all([not walker_thread.is_alive() for walker_thread in walker_thread_list]):
            # if all walkers are done, stop the simulation and the start frame
            self.simulation.stop()
            self.start_frame.stop()
        else:
            # if the walkers are still running, wait for 50 ms and check again
            self.after(50, self.wait_to_stop, walker_thread_list)

    def update_speed(self, value: float) -> None:
        """
        Updates the speed of the simulation.

        Args:
            value (float): The new speed value.

        Returns:
            None
        """
        self.simulation.update_speed(value)

    def update_simulation_count(self, value: int) -> None:
        """
        Updates the simulation count with the given value.

        Parameters:
            value (int): The new simulation count value.
        """
        self.simulation.set_simulation_count(value)

    def get_simulation_count(self) -> int:
        """
        Returns the simulation count.

        Returns:
            int: The simulation count.
        """
        return self.simulation.get_simulation_count()

    def update_max_steps(self, value: int) -> None:
        """
        Updates the maximum number of steps for the simulation.

        Args:
            value (int): The new maximum number of steps.
        """
        self.simulation.set_max_steps(value)

    def get_max_steps(self) -> int:
        """
        Returns the maximum number of steps for the simulation.

        Returns:
            int: The maximum number of steps.
        """
        return self.simulation.get_max_steps()

    def parse_config(self, path: str) -> bool:
        """
        Parses the configuration file at the given path and updates the simulation settings.

        Args:
            path (str): The path to the configuration file.

        Returns:
            bool: True if the configuration was successfully parsed and applied, False otherwise.
        """
        return self.simulation.config(path)
