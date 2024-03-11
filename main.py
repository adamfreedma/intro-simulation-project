import customtkinter as CTk
from main_frame import MainFrame
from simulation import Simulation
from grid import Grid
from screen import Screen


class MainApp(CTk.CTk):

    BUTTON_COLOR = "#009B44"
    BUTTON_HOVER_COLOR = "#007B34"

    RED_BUTTON_COLOR = "#DD1111"
    RED_BUTTON_HOVER_COLOR = "#AA0000"

    def __init__(self) -> None:
        CTk.CTk.__init__(self)

        self.title("Random walk")

        self._frame = None

        self._config_window()
        self.screen = Screen(800, 600)
        self.grid = Grid()
        self.simulation = Simulation(self.grid, self.screen, "temp.png")

        self.main_frame = MainFrame(self, self.simulation)

        self.bind("<Escape>", self.confirm_menu)

        self.switch_frame(self.main_frame)

    def _config_window(self) -> None:
        """configures propterties of the window"""

        self.width = 800
        self.height = 600

    def clear(self):
        if self._frame:
            self._frame.pack_forget()

    def switch_frame(self, frame):
        """Destroys current frame and replaces it with a new one."""
        self.clear()

        self._frame = frame
        self._frame.pack(expand=True, fill="both")

    def close(self, _=None):
        self.destroy()

    def confirm_menu(self, _=None):
        if not self.confirm_menu_open:
            self.confirm_menu_open = True

            self.top = CTk.cTkToplevel(self)
            self.top.attributes("-topmost", "true")
            self.top.overrideredirect(1)

            question_label = CTk.cTkLabel(
                self.top, text="Are you sure you want to quit?", font=self.font
            )

            yes_button = CTk.cTkButton(
                self.top,
                text="Yes",
                font=self.font,
                command=self.close,
                fg_color=self.BUTTON_COLOR,
                hover_color=self.BUTTON_HOVER_COLOR,
            )
            no_button = CTk.cTkButton(
                self.top,
                text="No",
                font=self.font,
                command=self.close_confirm_menu,
                fg_color=self.RED_BUTTON_COLOR,
                hover_color=self.RED_BUTTON_HOVER_COLOR,
            )

            question_label.grid(
                row=0, column=0, columnspan=2, padx=self.padding, pady=self.padding
            )
            yes_button.grid(row=1, column=0, padx=self.padding, pady=self.padding)
            no_button.grid(row=1, column=1, padx=self.padding, pady=self.padding)

    def close_confirm_menu(self):
        self.confirm_menu_open = False
        self.top.destroy()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
