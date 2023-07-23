# smolPaint GUI
# Tiny paint program for 5x5 NeoPixel BFF Grid displays
# by Krzysztof Krystian Jankowski
# (c) 2023/07

import tkinter as tk
from tkinter import ttk, Scale, font

class smolPaint:
    def __init__(self):
        # Create a window
        self.window = tk.Tk()
        self.window.title("smolPaint")
        self.window.geometry('320x260') # Set the window size to 800x600
        self.window.resizable(False, False)
        self.custom_font = font.Font(family="IBM 3270", size=10)
        self.window.option_add("*Font", self.custom_font)
        self.window.configure(bg="#222222")

        # Create frames with padding
        self.pixel_frame = tk.Frame(self.window, padx=10, pady=10)
        self.pixel_frame.pack()

        # Create Tab Control
        self.tab_control = ttk.Notebook(self.window)

        # Create tabs
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='Primary Color')

        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text='Secondary Color')

        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab3, text='NeoPixel')

        self.tab_tools = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_tools, text='Clear')

        self.tab_control.pack(expand=1, fill="both")

        self.brightness_slider = Scale(self.tab3, from_=0, to=100, orient='horizontal', label='Brightness (%)')
        self.brightness_slider.set(10)
        self.brightness_slider.grid(row=0, column=0, padx=5, pady=4, sticky='ns')
        self.brightness_slider.bind("<ButtonRelease-1>", self.update_pixel_stream)

        self.pixel_stream_frame = ttk.Frame(self.tab3)
        self.pixel_stream_frame.grid(row=0, column=1, padx=5, pady=4)

        # Create a string representation of the pixel colors
        self.pixel_stream = ["0,0,0"]*25  # Initialize all pixels as black
        self.pixel_colors = tk.StringVar()
        self.pixel_colors.set(",".join(self.pixel_stream))  # Display black for all pixels initially
        self.pixel_colors_entry = tk.Entry(self.pixel_stream_frame, textvariable=self.pixel_colors, state='readonly', width=24)
        self.pixel_colors_entry.pack(pady=4)

        self.copy_button = tk.Button(self.pixel_stream_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack(pady=4)

        self.white_button = tk.Button(self.tab_tools, text="Clear to White", command=lambda: self.clear_grid("white"))
        self.black_button = tk.Button(self.tab_tools, text="Clear to Black", command=lambda: self.clear_grid("black"))
        self.white_button.config(bg="white",fg="black")
        self.black_button.config(bg="black",fg="white")

        self.white_button.pack(side='left', padx=5)
        self.black_button.pack(side='left', padx=5)

        # Define a 5x5 grid of buttons
        self.buttons = []
        for i in range(5):
            row = []
            for j in range(5):
                button = tk.Button(self.pixel_frame, width=1, height=1, bg="black", bd=0)
                button.grid(row=i, column=j, padx=0, pady=0)
                row.append(button)
            self.buttons.append(row)

        self.controls = {}

        for idx, tab in enumerate([self.tab1, self.tab2]):
            slider_R = Scale(tab, from_=0, to=255, orient='horizontal', label='Red', width=20)
            slider_G = Scale(tab, from_=0, to=255, orient='horizontal', label='Green', width=20)
            slider_B = Scale(tab, from_=0, to=255, orient='horizontal', label='Blue', width=20)

            slider_R.set((1-idx)*255)
            slider_G.set((1-idx)*255)
            slider_B.set((1-idx)*255)

            slider_R.grid(row=0, column=0)
            slider_G.grid(row=0, column=1)
            slider_B.grid(row=0, column=2)

            prev_color = "white"
            if idx==1:
                prev_color = "black"
            color_preview = tk.Label(tab, text=" ", bg=prev_color, width=24)
            color_preview.grid(row=1, column=0, columnspan=3)

            self.controls[idx] = {
                'slider_R': slider_R,
                'slider_G': slider_G,
                'slider_B': slider_B,
                'color_preview': color_preview
            }

            for color in ['R', 'G', 'B']:
                    self.controls[idx]['slider_'+color].bind("<ButtonRelease-1>",lambda event, idx=idx: self.update_color_preview(idx, event))

        for i in range(5):
            for j in range(5):
                self.buttons[i][j].bind('<Button-1>', lambda event, i=i, j=j: self.change_color(i, j, 0))  # 0 - primary color
                self.buttons[i][j].bind('<Button-3>', lambda event, i=i, j=j: self.change_color(i, j, 1))  # 1 - secondary color

    def update_pixel_stream(self, event=None):
        brightness = self.brightness_slider.get() / 100.0  # Convert percentage to ratio
        adjusted_pixel_stream = []
        for pixel in self.pixel_stream:
            R, G, B = map(int, pixel.split(','))
            R = int(R * brightness)
            G = int(G * brightness)
            B = int(B * brightness)
            adjusted_pixel_stream.append(",".join([str(R), str(G), str(B)]))

        self.pixel_colors.set(",".join(adjusted_pixel_stream))
        self.pixel_colors_entry.update()

    def copy_to_clipboard(self):
        self.window.clipboard_clear()
        self.window.clipboard_append(self.pixel_colors.get())

    def clear_grid(self, color):
        for i in range(5):
            for j in range(5):
                self.buttons[i][j].config(bg=color)

        if color=="black":
            self.pixel_stream = ["0,0,0"]*25
        if color=="white":
            self.pixel_stream = ["255,255,255"]*25

        self.update_pixel_stream()

    def update_color_preview(self, idx, _):
        R = self.controls[idx]['slider_R'].get()
        G = self.controls[idx]['slider_G'].get()
        B = self.controls[idx]['slider_B'].get()
        color = '#%02x%02x%02x' % (R, G, B)
        self.controls[idx]['color_preview'].config(bg=color)


    def change_color(self, i, j, idx):
        R = self.controls[idx]['slider_R'].get()
        G = self.controls[idx]['slider_G'].get()
        B = self.controls[idx]['slider_B'].get()

        color = '#%02x%02x%02x' % (R, G, B)
        self.buttons[i][j].config(bg=color)

        # Update the pixel color in the pixel stream
        self.pixel_stream[j*5+i] = f"{R},{G},{B}"
        self.update_pixel_stream()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    paint = smolPaint()
    paint.run()

