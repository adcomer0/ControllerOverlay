import tkinter
from tkinter import ttk, colorchooser
import pygame
import os
from src.Visualizer import Visualizer
import main_assets.assets as gamepad_assets

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

# Constants
COLOUR_KEY = (255, 0, 128)  # fuchsia

supported_gps = ('PlayStation 4', 'Xbox One', 'Wolverine', 'Mouse and Keyboard')
assets = None
gp_using = None
should_continue = False
platform_map = {
    2: (gamepad_assets.WolverineAssets, 'wolverine'),
    1: (gamepad_assets.Xbox1Assets, 'xbox1'),
    0: (gamepad_assets.PS4Assets, 'ps4'),
    3: (gamepad_assets.MouseKeyboardAssets, 'mouse_keyboard')
}

root = tkinter.Tk()
root.geometry('300x200')
root.title('Gamepad Overlay Launcher')
lbl = tkinter.Label(root, text='Gamepad: ', font=('lucon.ttf', 18))
choices = ttk.Combobox(root, values=supported_gps)
choices.current(2)  # Set default selection to Wolverine

lbl.grid(column=0, row=0)
choices.grid(column=1, row=0)

def get_colour():
    global COLOUR_KEY
    col = colorchooser.askcolor()
    COLOUR_KEY = col[0]

def gp_launch():
    global assets, gp_using, should_continue
    idx = choices.current()
    data = platform_map[idx]
    assets = data[0]()
    gp_using = data[1]
    should_continue = True
    root.destroy()

set_colour = tkinter.Button(root, text='Set Background Colour', command=get_colour)
set_colour.grid(column=1, row=1)
transparent_var = tkinter.BooleanVar()
transparent_checkbox = tkinter.Checkbutton(root, text="Transparent Bottom Left", variable=transparent_var)
transparent_checkbox.grid(column=1, row=2)
launch = tkinter.Button(root, text='Launch', command=gp_launch)
launch.grid(column=1, row=3)

root.mainloop()
if should_continue:
    app = Visualizer(assets, gp_using, transparent=transparent_var.get())
    app.run()
    pygame.quit()
