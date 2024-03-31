import customtkinter as ctk  # type: ignore[import]
from walker_frame import WalkerFrame
from typing import List
from walker import Walker


class WalkerConfigFrame(ctk.CTkFrame):  # type: ignore[misc]

    __MAX_WALKERS = 5

    def __init__(self, master: ctk.CTkFrame) -> None:
        """
        Initialize the WalkerConfigFrame.

        Args:
            master (ctk.CTkFrame): The master frame to which this frame belongs.
        """
        ctk.CTkFrame.__init__(self, master, corner_radius=15)

        self.height = master.height
        self.width = master.width
        self.widget_width = self.width // 8
        self.padding = master.padding

        self.walker_frame_list: List[WalkerFrame] = []

        self.add_walker_button = ctk.CTkButton(
            self, self.widget_width, text="Add walker", command=self.create_walker
        )

        # layout
        self.add_walker_button.pack(padx=self.padding, pady=self.padding)

    def create_walker(self) -> None:
        """
        Creates a new WalkerFrame and adds it to the walker_frame_list.
        """
        walker_frame = WalkerFrame(self)
        self.walker_frame_list.append(walker_frame)
        walker_frame.pack(padx=self.padding, pady=self.padding)

        if len(self.walker_frame_list) >= self.__MAX_WALKERS:
            self.add_walker_button.configure(state="disabled")

    def delete_walker(self, walker_frame: WalkerFrame) -> None:
        """
        Deletes a walker frame from the walker frame list.

        Args:
            walker_frame (WalkerFrame): The walker frame to be deleted.
        """
        if walker_frame in self.walker_frame_list:
            self.walker_frame_list.remove(walker_frame)

        self.add_walker_button.configure(state="normal")

    def get_walkers(self) -> List[Walker]:
        """
        Returns a list of Walker objects corresponding to the walker frames in the walker_frame_list.

        Returns:
            List[Walker]: A list of Walker objects.
        """
        return [
            frame.get_walker(str(num))
            for num, frame in enumerate(self.walker_frame_list)
        ]
