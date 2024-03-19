import customtkinter as CTk
from main_frame import MainFrame
from graph_viewer_frame import GraphViewerFrame
from simulation import Simulation
from grid import Grid
from screen import Screen
import customtkinter as ctk
from typing import Any

class MainApp(CTk.CTk): # type: ignore[misc]

    BUTTON_COLOR = "#009B44"
    BUTTON_HOVER_COLOR = "#007B34"

    RED_BUTTON_COLOR = "#DD1111"
    RED_BUTTON_HOVER_COLOR = "#AA0000"

    def __init__(self) -> None:
        CTk.CTk.__init__(self)

        self.title("Random walk")

        self.confirm_menu_open = False
        self.padding = 10

        self._config_window()
        self.screen = Screen(800, 600)
        self.grid = Grid()
        self.simulation = Simulation(self.grid, self.screen)
        

        self.tab_menu = ctk.CTkTabview(self)
        self.tab_list = []
        self.tab_list.append(self.tab_menu.add("Simulation"))
        self.tab_list.append(self.tab_menu.add("Graph viewer"))
        
        self.main_frame = MainFrame(self.tab_list[0], self, self.simulation)
        self.graph_viewer_frame = GraphViewerFrame(self.tab_list[1], self)
        
        self.main_frame.pack()
        self.graph_viewer_frame.pack()

        self.tab_menu.configure(command=self.graph_viewer_frame.update_folders_list)
        self.bind("<Escape>", self.confirm_menu)

        self.tab_menu.pack()

    def _config_window(self) -> None:
        """configures propterties of the window"""

        self.width = 800
        self.height = 600

    def close(self, _:Any=None) -> None:
        self.destroy()

    def confirm_menu(self, _:Any=None) -> None:
        if not self.confirm_menu_open:
            self.confirm_menu_open = True

            self.top = CTk.CTkToplevel(self)
            self.top.attributes("-topmost", "true")
            self.top.overrideredirect(1)

            question_label = CTk.CTkLabel(
                self.top, text="Are you sure you want to quit?",
            )

            yes_button = CTk.CTkButton(
                self.top,
                text="Yes",
                command=self.close,
            )
            no_button = CTk.CTkButton(
                self.top,
                text="No",
                command=self.close_confirm_menu,
            )

            question_label.grid(
                row=0, column=0, columnspan=2, padx=self.padding, pady=self.padding
            )
            yes_button.grid(row=1, column=0, padx=self.padding, pady=self.padding)
            no_button.grid(row=1, column=1, padx=self.padding, pady=self.padding)

    def close_confirm_menu(self) -> None:
        self.confirm_menu_open = False
        self.top.destroy()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = MainApp()
    app.mainloop()
