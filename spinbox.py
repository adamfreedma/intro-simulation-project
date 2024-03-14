import customtkinter
from typing import Callable

class Spinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 starting_value: int = 0,
                 max_value: int = 999,
                 min_value: int = 0,
                 text: str = None,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.command = command
        self.max_value = max_value
        self.min_value = min_value

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(10, 0), pady=3)

        self.entry_var = customtkinter.StringVar(value=str(starting_value))
        self.entry = customtkinter.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0, textvariable=self.entry_var)
        self.entry.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 10), pady=3)
        
        if text:
            self.text_label = customtkinter.CTkLabel(self, width, text=text)
            self.text_label.grid(row=1, column=0, columnspan=3, padx=20, pady=3)

        # write listener
        self.entry_var.trace_add("write", lambda *args: self.cap_write_values(self.entry_var))

    def add_button_callback(self):
        try:
            value = min(int(self.entry.get()) + 1, self.max_value)
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return
        if self.command is not None and self.get():
            self.command(int(self.get()))

    def subtract_button_callback(self):
        try:
            value = max(int(self.entry.get()) - 1, self.min_value)
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return
        if self.command is not None and self.get():
            self.command(int(self.get()))

    def cap_write_values(self, text_var: customtkinter.StringVar):
        if text_var.get().isnumeric():
            if int(text_var.get()) > self.max_value:
                text_var.set(str(self.max_value))
            if int(text_var.get()) < self.min_value:
                text_var.set(str(self.min_value))
        if self.command is not None and self.get():
            self.command(int(self.get()))

    def get(self) -> int:
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))