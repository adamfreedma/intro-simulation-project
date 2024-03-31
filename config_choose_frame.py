import customtkinter as ctk  # type: ignore[import]
from colors import Colors
import os
from typing import Optional


class ConfigChooseFrame(ctk.CTkFrame):  # type: ignore[misc]

    def __init__(self, master: ctk.CTkFrame) -> None:
        """
        Initializes an instance of the ConfigChooseFrame class.

        Args:
            master (MainFrame): The main frame.

        Returns:
            None
        """
        ctk.CTkFrame.__init__(self, master, corner_radius=15)

        self.height = master.height
        self.width = master.width
        self.widget_width = self.width // 8
        self.padding = master.padding

        self.file_picker = ctk.CTkButton(
            self,
            self.widget_width,
            text="Enter config file",
            command=self.file_dialog,
        )

        # layout
        self.file_picker.pack(expand=True, padx=self.padding, pady=self.padding)

    def file_dialog(self, open: Optional[bool] = True) -> None:
        """
        Opens a file dialog to select a configuration file.

        Args:
            open (bool, optional): If True, opens the file dialog for selecting a file to open.
                If False, dose not open the file dialog.

        Returns:
            None

        """
        success = False
        if open:
            success = self.master.parse_config(
                ctk.filedialog.askopenfilename(
                    initialdir=os.getcwd(),
                    title="Enter the config file",
                    filetypes=[("JSON", "*.json")],
                )
            )
        # colors the button based on the success of reading the file and the file format
        if success:
            self.file_picker.configure(fg_color=Colors.GREEN)
        else:
            self.file_picker.configure(fg_color=Colors.RED)
