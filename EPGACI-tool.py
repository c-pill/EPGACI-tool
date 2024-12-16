from EPGACI import EPGACI
from tkinter import filedialog
import tkinter as tk

class EPGACI_GUI:
    image_selected = False

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("EPGACI tool")

        # default values for EPGACI
        self.N = tk.IntVar(value=15)
        self.generations = tk.IntVar(value=50)
        self.goal = tk.DoubleVar(value=50)
        self.image = tk.PhotoImage(file="images/No Image Selected.png")

        self.pop_label = tk.Label(self.window, text=f"Number of Individuals in Population: {self.N.get()}", font=("Courier", 9))
        self.gen_label = tk.Label(self.window, text=f"Number of Generations to Compute: {self.generations.get()}", font=("Courier", 9))
        self.gen_note_label = tk.Label(self.window, text="*at least 50 generations recommended\nto ensure accurate results", font=("Courier", 8))
        self.goal_label = tk.Label(self.window, text=f"Goal % Similar: {self.goal.get()}", font=("Courier", 9))
        self.image_label = tk.Label(self.window, image=self.image)

        self.pop_scale = tk.Scale(self.window, variable=self.N, from_=1, to=50, orient="horizontal")
        self.gen_scale = tk.Scale(self.window, variable=self.generations, from_=1, to=300, orient="horizontal")
        self.goal_scale = tk.Scale(self.window, variable=self.goal, from_=0, to=100, orient="horizontal")

        self.select_image_button = tk.Button(self.window, text="Select Image to Censor")
        self.start_button = tk.Button(self.window, text="Start EPGACI")

        self.pop_scale.pack()
        self.pop_label.pack()

        self.gen_scale.pack()
        self.gen_label.pack()
        self.gen_note_label.pack()

        self.goal_scale.pack()
        self.goal_label.pack()

        self.image_label.pack()

        self.select_image_button.pack()

    def update_population(self, args):
        self.pop_label.configure(text=f"Number of Individuals in Population: {self.N.get()}")

    def update_generations(self, args):
        self.gen_label.configure(text=f"Number of Generations to Compute: {self.generations.get()}")

    def update_goal(self, args):
        self.goal_label.configure(text=f"Goal % Similar: {self.goal.get()}")

    def update_image(self):
        self.image_label.configure(image=self.image)

    def update_counter(self, args):
        self.counter_label.configure(text=f"Generations: {self.counter.get()} / {self.generations.get()}")
        if self.counter.get() == self.generations.get(): self.counter_label.pack_forget()

    def select_image(self):
        # fix EPGACI to allow for other image types
        self.image_file = filedialog.askopenfilename(
            filetypes=[
                ("PNG images", "*.png")
            ]
        )
        if self.image_file != '':
            self.image = tk.PhotoImage(file=self.image_file).subsample(2,2)
            self.update_image()
            if self.image_selected is False:
                self.start_button = tk.Button(self.window, text="Start EPGACI", command=self.start)
                self.start_button.pack()
                self.image_selected = True
        else: 
            self.image = tk.PhotoImage(file="images/No Image Selected.png")
            if self.image_selected is True:
                self.start_button.pack_forget()
                self.image_selected = False
            self.update_image()



    def start(self):
        EPGACI(self.N.get(), self.goal.get(), self.generations.get(), self.image_file).run()

    def configure_commands(self):
        self.pop_scale.configure(command=self.update_population)
        self.gen_scale.configure(command=self.update_generations)
        self.goal_scale.configure(command=self.update_goal)
        self.select_image_button.configure(command=self.select_image)
        self.start_button.configure(command=self.start)

gui = EPGACI_GUI()
gui.configure_commands()
gui.window.mainloop()