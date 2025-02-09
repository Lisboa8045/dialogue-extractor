from tkinter import *
from tkinter import ttk, filedialog
from DialogueExtractor import extract_dialogue

class App(Tk):

    def __init__(self):
        super().__init__()
        # Title
        self.title("Dialogue Extractor")

        # Mainframe
        self.mainframe = ttk.Frame(self, padding="3 3 102 102")
        self.mainframe.grid(column=0, row=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Subtitles
        ttk.Label(self.mainframe, text="Path to Subtitles:").grid(column=1, row=1, sticky=W)
        self.subs_path = StringVar()
        self.subs_path.set("No file selected")
        ttk.Label(self.mainframe, textvariable=self.subs_path).grid(column=2, row=1, sticky=(W, E))
        ttk.Button(self.mainframe, text="Find Subs", command=self.select_sub_file).grid(column=3, row=1, sticky=W)

        # Video
        ttk.Label(self.mainframe, text="Path to Video:").grid(column=1, row=2, sticky=E)
        self.video_path = StringVar()
        self.video_path.set("No file selected")
        ttk.Label(self.mainframe, textvariable=self.video_path).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(self.mainframe, text="Find Video", command=self.select_video_file).grid(column=3, row=2, sticky=W)

        # Output Folder
        ttk.Label(self.mainframe, text="Path to Result:").grid(column=1, row=3, sticky=E)
        self.result_path = StringVar()
        ttk.Label(self.mainframe, textvariable=self.result_path).grid(column=2, row=3, sticky=(W, E))
        ttk.Button(self.mainframe, text="Select Output Folder", command=self.select_output_folder).grid(column=3, row=3, sticky=W)

        # Resulting Audio file name
        self.output_file = StringVar()
        ttk.Label(self.mainframe, text="Output Name:").grid(column=1, row=4, sticky=E)
        self.output_file_entry = ttk.Entry(self.mainframe, textvariable=self.output_file)
        self.output_file_entry.grid(column=2, row=4, sticky=(W, E))

        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        # Start Button
        ttk.Button(self.mainframe, text="Start Conversion", command=self.calculate).grid(column=2, row=5, sticky=W)
        

    def calculate(self):
        try:
            print("Command received...")
            extract_dialogue(self.subs_path.get(), self.video_path.get(), f"{self.result_path.get()}/{self.output_file.get()}.mp3")
        except ValueError:
            pass

    def select_sub_file(self):
        path = filedialog.askopenfilename(title="Select a Subtitle file",
                                                    filetypes=[("Subtitle Files", "*.srt *.ass"), ("All File Types", "*.*")])
        if path:
            self.subs_path.set(path)
        
    def select_video_file(self):
        path = filedialog.askopenfilename(title="Select a Video file",
                                                    filetypes=[("Video Files", "*.mkv *.mp4 *.mov"), ("All File Types", "*.*")])
        if path:
            self.video_path.set(path)
            self.output_file.set(path.split("/")[-1].split(".")[0])

    def select_output_folder(self):
        path = filedialog.askdirectory(title="Select the Output folder")
        if path:
            self.result_path.set(path)


app = App()
app.mainloop()