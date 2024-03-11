import customtkinter as ctk
import colors
import os


class ConfigChooseFrame(ctk.CTkFrame):

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master, corner_radius=15)

        self.height = master.height
        self.width = master.width
        self.widget_width = self.width // 8

        self.teleporters_file_picker = ctk.CTkButton(
            self,
            self.widget_width,
            text="Choose Teleporter config",
            command=self.teleporters_file_dialog,
        )

        self.obstacles_file_picker = ctk.CTkButton(
            self,
            self.widget_width,
            text="Choose Obstacle config",
            command=self.obstacles_file_dialog,
        )

        # layout
        self.teleporters_file_picker.pack(expand=True)
        self.obstacles_file_picker.pack(expand=True)

    def teleporters_file_dialog(self):
        success = self.master.parse_teleporters_config(
            ctk.filedialog.askopenfilename(
                initialdir=os.getcwd(),
                title="Enter the teleporters file config",
                filetypes=[("JSON", "*.json")],
            )
        )

        if success:
            self.teleporters_file_picker.configure(fg_color=colors.GREEN)
        else:
            self.teleporters_file_picker.configure(fg_color=colors.RED)

    def obstacles_file_dialog(self):
        success = self.master.parse_obstacles_config(
            ctk.filedialog.askopenfilename(
                initialdir=os.getcwd(),
                title="Enter the obstacles file config",
                filetypes=[("JSON", "*.json")],
            )
        )

        if success:
            self.obstacles_file_picker.configure(fg_color=colors.GREEN)
        else:
            self.obstacles_file_picker.configure(fg_color=colors.RED)
