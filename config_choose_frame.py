import customtkinter as ctk # type: ignore[import]
import colors
import os
from typing import Optional


class ConfigChooseFrame(ctk.CTkFrame): # type: ignore[misc]

    def __init__(self, master: ctk.CTkFrame) -> None:
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

    def file_dialog(self, open: Optional[bool]=True) -> None:
        success = False
        if open:
            success = self.master.parse_config(
                ctk.filedialog.askopenfilename(
                    initialdir=os.getcwd(),
                    title="Enter the config file",
                    filetypes=[("JSON", "*.json")],
                )
            )

        if success:
            self.file_picker.configure(fg_color=colors.GREEN)
        else:
            self.file_picker.configure(fg_color=colors.RED)

