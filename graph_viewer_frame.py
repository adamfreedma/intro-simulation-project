import customtkinter as ctk
from PIL import Image, ImageTk
import os

class GraphViewerFrame(ctk.CTkFrame):

    def __init__(self, tab_master, master):
        ctk.CTkFrame.__init__(self, tab_master, corner_radius=15)

        self.height = master.height
        self.width = master.width
        self.widget_width = self.width // 8
        self.padding = master.padding
        
        self.__paths = []
        self.__path_index = 0
        
        self.__folder_var = ctk.StringVar()

        self.image = ctk.CTkLabel(self, image=None, text="")
        
        self.buttons_frame = ctk.CTkFrame(self)
        self.folder_entry = ctk.CTkEntry(self.buttons_frame, self.widget_width, textvariable=self.__folder_var)
        self.next_button = ctk.CTkButton(self.buttons_frame, self.widget_width, text="->", command=self.next_image)
        self.prev_button = ctk.CTkButton(self.buttons_frame, self.widget_width, text="<-", command=self.prev_image)
        
        # layout
        self.buttons_frame.pack(padx=self.padding, pady=self.padding)
        self.prev_button.pack(side="left", expand=True, padx=self.padding, pady=self.padding)
        self.folder_entry.pack(side="left", expand=True, padx=self.padding, pady=self.padding)
        self.next_button.pack(side="left", expand=True, padx=self.padding, pady=self.padding)
        
        self.image.pack(padx=self.padding, pady=self.padding)

        # folder entry listener
        self.__folder_var.trace_add("write", lambda *args: self.update_paths())

        
    def next_image(self):
        self.__path_index += 1
        self.update_image()
        
    def prev_image(self):
        self.__path_index -= 1
        self.update_image()
        
    def update_paths(self):
        print(self.__folder_var.get())
        if os.path.isdir(self.__folder_var.get()):
            self.__paths = [f"{self.__folder_var.get()}/{path}" for path in os.listdir(self.__folder_var.get()) if path.endswith(".png")]
            self.__path_index = 0
            self.update_image()
        
    def update_image(self):
        if self.__paths and os.path.exists(self.__paths[self.__path_index % len(self.__paths)]):
            img = ctk.CTkImage(dark_image=Image.open(self.__paths[self.__path_index % len(self.__paths)]), size=(self.width, self.height))
            self.image.configure(image=img)
        