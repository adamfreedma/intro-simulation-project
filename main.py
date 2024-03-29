import customtkinter as CTk  # type: ignore[import]
from main_frame import MainFrame
from graph_viewer_frame import GraphViewerFrame
from simulation import Simulation
from grid import Grid
from screen import Screen
import customtkinter as ctk
from typing import Any, Optional


class MainApp(CTk.CTk):  # type: ignore[misc]

    def __init__(self) -> None:
        """
        Initializes the main application window.
        """
        CTk.CTk.__init__(self)

        self.title("Random walk")

        self.confirm_menu_open = False
        self.padding = 10
        self.closed = False

        # configures the screen and simulation
        self._config_window()
        self.screen = Screen(800, 600)
        self.grid = Grid()
        self.simulation = Simulation(self.grid, self.screen)

        # initializes the frames
        self.tab_menu = ctk.CTkTabview(self)
        self.tab_list = []
        self.tab_list.append(self.tab_menu.add("Simulation"))
        self.tab_list.append(self.tab_menu.add("Graph viewer"))

        self.main_frame = MainFrame(self.tab_list[0], self, self.simulation)
        self.graph_viewer_frame = GraphViewerFrame(self.tab_list[1], self)

        # layout
        self.main_frame.pack()
        self.graph_viewer_frame.pack()

        # bins the tab menu to the update_folders_list method
        self.tab_menu.configure(command=self.graph_viewer_frame.update_folders_list)
        # adds a key binding to the escape key to open the exit confirm menu
        self.bind("<Escape>", self.confirm_menu)

        self.tab_menu.pack()

    def _config_window(self) -> None:
        """configures propterties of the window"""

        self.width = 800
        self.height = 600

    def close(self, _: Any = None) -> None:
        """
        Closes the application window.

        Args:
            _: Optional argument (ignored).
        """
        self.destroy()
        self.closed = True

    def confirm_menu(self, _: Optional[Any] = None) -> None:
        """
        Opens a confirmation menu asking the user if they really want to quit.

        Args:
            _: Optional argument, not used in the method.
        """
        if not self.confirm_menu_open:
            self.confirm_menu_open = True

            # creates the window
            self.top = CTk.CTkToplevel(self)
            self.top.attributes("-topmost", "true")
            self.top.overrideredirect(1)
            # adding the label and buttons
            question_label = CTk.CTkLabel(
                self.top,
                text="Are you sure you want to quit?",
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
        """
        Closes the confirm menu.
        """
        self.confirm_menu_open = False
        self.top.destroy()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = MainApp()
    app.mainloop()
