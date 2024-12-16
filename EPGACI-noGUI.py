from EPGACI import EPGACI
from tkinter import filedialog

N = 15
goal = 75
# in gui, do 50 each time. option to continue to perform additional 50
generations = 50
# fix EPGACI to allow for other image types
image = filedialog.askopenfilename(
    filetypes=[
        ("PNG images", "*.png")
    ]
)

# N: population of generations, goal %, generations, image path
EPGACI(N, goal, generations, image).run()