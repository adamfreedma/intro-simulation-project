import customtkinter as ctk # type: ignore[import]
from typing import Callable, Optional, Any

class Spinbox(ctk.CTkFrame): # type: ignore[misc]
    def __init__(self, *args: Any,
                 width: int=100,
                 height: int=32,
                 starting_value: int=0,
                 max_value: int=999,
                 min_value: int=0,
                 text: str="",
                 command: Optional[Callable[[int], None]]=None,
                 **kwargs: Any) -> None:
        """
        Initialize a Spinbox object.

        Args:
            *args: Variable length argument list.
            width (int): The width of the Spinbox.
            height (int): The height of the Spinbox.
            starting_value (int): The initial value of the Spinbox.
            max_value (int): The maximum value of the Spinbox.
            min_value (int): The minimum value of the Spinbox.
            text (str): The text to display below the Spinbox.
            command (Optional[Callable[[int], None]]): A callback function to execute when the value of the Spinbox changes.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        super().__init__(*args, width=width, height=height, **kwargs)

        self.command = command
        self.max_value = max_value
        self.min_value = min_value

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = ctk.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(10, 0), pady=3)
        # initialize entry
        self.entry_var = ctk.StringVar(value=str(starting_value))
        self.entry = ctk.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0, textvariable=self.entry_var)
        self.entry.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky="ew")
        # initialize add button
        self.add_button = ctk.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 10), pady=3)
        
        if text:
            self.text_label = ctk.CTkLabel(self, width, text=text)
            self.text_label.grid(row=1, column=0, columnspan=3, padx=20, pady=3)

        # write listener
        self.entry_var.trace_add("write", lambda *args: self.cap_write_values(self.entry_var))

    def add_button_callback(self) -> bool:
        """
        Increments the value in the Spinbox entry by 1 and updates the entry field.
        If a command is provided and the Spinbox has a value, the command is called with the new value.
        
        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            # increment value
            value = min(int(self.entry.get()) + 1, self.max_value)
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return False
        
        # call command if provided
        if self.command is not None and self.get():
            self.command(int(self.get()))
        
        return True

    def subtract_button_callback(self) -> bool:
        """
        Decreases the value in the entry field by 1 and updates the entry field accordingly.
        If a command is provided and the entry field has a valid value, the command is called with the new value.
        
        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            # decrement value
            value = max(int(self.entry.get()) - 1, self.min_value)
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return False

        # call command if provided
        if self.command is not None and self.get():
            self.command(int(self.get()))

        return True

    def cap_write_values(self, text_var: ctk.StringVar) -> None:
        """
        Caps the value of the text_var within the specified range.
        
        Args:
            text_var (ctk.StringVar): The StringVar object containing the value to be capped.
        
        Returns:
            None
        """
        if text_var.get().isnumeric():
            # cap values
            if int(text_var.get()) > self.max_value:
                text_var.set(str(self.max_value))
                self.entry.delete(0, "end")
                self.entry.insert(0, str(self.max_value))
            if int(text_var.get()) < self.min_value:
                text_var.set(str(self.min_value))
                self.entry.delete(0, "end")
                self.entry.insert(0, str(self.min_value))

        # call command if provided
        if self.command is not None and self.get():
            self.command(int(self.get()))

    def get(self) -> int:
        """
        Get the value of the spinbox.

        Returns:
            int: The value of the spinbox as an integer. If the value cannot be converted to an integer, 0 is returned.
        """
        try:
            return int(self.entry.get())
        except ValueError:
            return 0

    def set(self, value: int) -> None:
        """
        Sets the value of the spinbox.

        Parameters:
            value (int): The new value to be set.
        """
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))