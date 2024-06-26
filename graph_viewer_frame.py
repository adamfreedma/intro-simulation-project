import customtkinter as ctk  # type: ignore[import]
from PIL import Image
import os
from typing import List, Optional


class GraphViewerFrame(ctk.CTkFrame):  # type: ignore[misc]

    __FOLDER_PREFIX = "GRAPHS"

    def __init__(self, tab_master: ctk.CTkFrame, master: ctk.CTkFrame) -> None:
        """
        Initializes the GraphViewerFrame object.

        Args:
            tab_master (ctk.CTkFrame): The parent frame for the GraphViewerFrame.
            master (MainApp): The main app.

        Returns:
            None
        """
        ctk.CTkFrame.__init__(self, tab_master, corner_radius=15)

        self.height = master.height
        self.width = master.width
        self.widget_width = self.width // 8
        self.padding = master.padding

        self.__paths: List[str] = []
        self.__path_index = 0

        self.__folder_var = ctk.StringVar()

        self.image = ctk.CTkLabel(self, image=None, text="")

        # layout of the buttons frame
        self.buttons_frame = ctk.CTkFrame(self)
        self.folder_entry = ctk.CTkComboBox(
            self.buttons_frame, self.widget_width, variable=self.__folder_var
        )
        self.next_button = ctk.CTkButton(
            self.buttons_frame, self.widget_width, text="->", command=self.next_image
        )
        self.prev_button = ctk.CTkButton(
            self.buttons_frame, self.widget_width, text="<-", command=self.prev_image
        )

        # layout
        self.buttons_frame.pack(padx=self.padding, pady=self.padding)
        self.prev_button.pack(
            side="left", expand=True, padx=self.padding, pady=self.padding
        )
        self.folder_entry.pack(
            side="left", expand=True, padx=self.padding, pady=self.padding
        )
        self.next_button.pack(
            side="left", expand=True, padx=self.padding, pady=self.padding
        )

        self.image.pack(padx=self.padding, pady=self.padding)

        # folder entry listener
        self.update_folders_list()
        self.__folder_var.trace_add("write", lambda *args: self.update_paths())

    @staticmethod
    def get_folder_prefix() -> str:
        """
        Returns the folder prefix used by the GraphViewerFrame class.

        Returns:
            str: The folder prefix used by the GraphViewerFrame class.
        """
        return GraphViewerFrame.__FOLDER_PREFIX

    def get_path_index(self) -> int:
        """
        Returns the current path index.

        Returns:
            int: The current path index.
        """
        return self.__path_index

    def next_image(self) -> None:
        """
        Moves to the next image in the folder and updates the image displayed.
        """
        self.__path_index += 1
        self.update_image()

    def prev_image(self) -> None:
        """
        Moves to the previous image in the folder and updates the image displayed.
        """
        self.__path_index -= 1
        self.update_image()

    def update_folders_list(self) -> None:
        """
        Updates the values in the folder_entry widget with the names of folders
        that contain the specified folder prefix.

        Returns:
            None
        """
        self.folder_entry.configure(
            values=[
                folder[0].split(self.__FOLDER_PREFIX)[-1]
                for folder in os.walk(os.getcwd())
                if folder[0].count(self.__FOLDER_PREFIX)
            ]
        )

    def update_paths(self, test: Optional[bool] = False) -> None:
        """
        Update the list of image paths based on the selected folder.

        Args:
            test (bool, optional): If True, clears the list of paths. Defaults to False.
        """
        folder_path = self.__FOLDER_PREFIX + self.__folder_var.get()
        if os.path.isdir(folder_path):
            self.__paths = [
                f"{folder_path}/{path}"
                for path in os.listdir(folder_path)
                if path.endswith(".png")
            ]
            self.__path_index = 0
            if test:
                self.__paths = []
            self.update_image()

    def update_image(self) -> None:
        """
        Updates the image displayed in the frame.

        If there are paths available and the current path exists, it opens the image at the current path
        and displays it in the frame.

        Returns:
            None
        """
        if self.__paths and os.path.exists(
            self.__paths[self.__path_index % len(self.__paths)]
        ):
            img = ctk.CTkImage(
                dark_image=Image.open(
                    self.__paths[self.__path_index % len(self.__paths)]
                ),
                size=(self.width, self.height),
            )
            self.image.configure(image=img)
