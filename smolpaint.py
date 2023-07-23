# smolPaint GUI
# Tiny paint program for 5x5 NeoPixel BFF Grid displays
# by Krzysztof Krystian Jankowski
# (c) 2023/07

import tkinter as tk
from tkinter import ttk, Scale, font

# Create a window
window = tk.Tk()
window.title("smolPaint by Krzysztof Krystian Jankowski")

custom_font = font.Font(family="IBM 3270", size=10)
window.option_add("*Font", custom_font)

# Create frames with padding
pixel_frame = tk.Frame(window, padx=10, pady=10)
pixel_frame.pack()

# Create Tab Control
tab_control = ttk.Notebook(window)

# Create tabs
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Primary Color')

tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Secondary Color')

tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text='NeoPixel')

tab_control.pack(expand=1, fill="both")

def update_pixel_stream():
    brightness = brightness_slider.get() / 100.0  # Convert percentage to ratio
    adjusted_pixel_stream = []
    for pixel in pixel_stream:
        R, G, B = map(int, pixel.split(','))
        R = int(R * brightness)
        G = int(G * brightness)
        B = int(B * brightness)
        adjusted_pixel_stream.append(",".join([str(R), str(G), str(B)]))

    pixel_colors.set(",".join(adjusted_pixel_stream))
    pixel_colors_entry.update()

brightness_slider = Scale(tab3, from_=0, to=100, orient='horizontal', label='Brightness (%)')
brightness_slider.set(40)
brightness_slider.grid(row=0, column=0, padx=5, pady=4, sticky='ns')
brightness_slider.bind("<ButtonRelease-1>", lambda _: update_pixel_stream())

pixel_stream_frame = ttk.Frame(tab3)
pixel_stream_frame.grid(row=0, column=1, padx=5, pady=4)

# Create a string representation of the pixel colors
pixel_stream = ["0,0,0"]*25  # Initialize all pixels as black
pixel_colors = tk.StringVar()
pixel_colors.set(",".join(pixel_stream))  # Display black for all pixels initially
pixel_colors_entry = tk.Entry(pixel_stream_frame, textvariable=pixel_colors, state='readonly', width=24)
pixel_colors_entry.pack(pady=4)

def copy_to_clipboard():
    window.clipboard_clear()
    window.clipboard_append(pixel_colors.get())

copy_button = tk.Button(pixel_stream_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(pady=4)


# Define a 5x5 grid of buttons
buttons = []
for i in range(5):
    row = []
    for j in range(5):
        button = tk.Button(pixel_frame, width=2, height=1, bg="black", bd=0)
        button.grid(row=i, column=j, padx=0, pady=0)
        row.append(button)
    buttons.append(row)

# Store the slider and color preview references in a dictionary
controls = {}

# Create color preview and sliders for both tabs
for idx, tab in enumerate([tab1, tab2]):
    slider_R = Scale(tab, from_=0, to=255, orient='horizontal', label='Red')
    slider_G = Scale(tab, from_=0, to=255, orient='horizontal', label='Green')
    slider_B = Scale(tab, from_=0, to=255, orient='horizontal', label='Blue')

    slider_R.grid(row=0, column=0)
    slider_G.grid(row=0, column=1)
    slider_B.grid(row=0, column=2)

    color_preview = tk.Label(tab, text=" ", bg="black", width=24)
    color_preview.grid(row=1, column=0, columnspan=3)

    controls[idx] = {
        'slider_R': slider_R,
        'slider_G': slider_G,
        'slider_B': slider_B,
        'color_preview': color_preview,
    }

# Function to update color preview
def update_color_preview(idx, _):
    R = controls[idx]['slider_R'].get()
    G = controls[idx]['slider_G'].get()
    B = controls[idx]['slider_B'].get()
    color = '#%02x%02x%02x' % (R, G, B)
    controls[idx]['color_preview'].config(bg=color)

# Bind sliders to color preview update function
for idx in controls:
    controls[idx]['slider_R'].bind("<ButtonRelease-1>", lambda event, idx=idx: update_color_preview(idx, event))
    controls[idx]['slider_G'].bind("<ButtonRelease-1>", lambda event, idx=idx: update_color_preview(idx, event))
    controls[idx]['slider_B'].bind("<ButtonRelease-1>", lambda event, idx=idx: update_color_preview(idx, event))

# Function to change color of a button
def change_color(button, i, j, idx):
    R = controls[idx]['slider_R'].get()
    G = controls[idx]['slider_G'].get()
    B = controls[idx]['slider_B'].get()

    color = '#%02x%02x%02x' % (R, G, B)
    button.config(bg=color)

    # Update the corresponding color in pixel_stream
    pixel_stream[5*j+i] = str(R) + "," + str(G) + "," + str(B)

    # Update the pixel colors with brightness adjustment
    update_pixel_stream()

# Add click event to buttons
for i in range(5):
    for j in range(5):
        buttons[i][j].bind('<Button-1>', lambda event, i=i, j=j, button=buttons[i][j]: change_color(button, i, j, 0))  # 0 - primary color
        buttons[i][j].bind('<Button-3>', lambda event, i=i, j=j, button=buttons[i][j]: change_color(button, i, j, 1))  # 1 - secondary color

window.mainloop()
