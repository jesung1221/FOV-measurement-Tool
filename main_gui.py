import tkinter as tk
from tkinter import StringVar, OptionMenu, Listbox, END, Menu, messagebox
from tkinter import Toplevel, Label
from fov_processing import process_measurements  # Import the process_measurements function
from PIL import Image, ImageTk  # Import for handling image icons

# Function to create a tooltip
def create_tooltip(widget, text):
    tooltip = None

    def enter(event):
        nonlocal tooltip
        tooltip = Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        label = Label(tooltip, text=text, background="light yellow", borderwidth=1, relief="solid")
        label.pack()

    def leave(event):
        nonlocal tooltip
        if tooltip:
            tooltip.destroy()
            tooltip = None

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

# Create the main application window
root = tk.Tk()
root.title("Field of View Measurement")

# Configure the root grid to allow for resizing
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=2)
root.grid_rowconfigure(2, weight=1)

# Chart Size Section
chart_frame = tk.LabelFrame(root, text="Chart Size", padx=10, pady=10)
chart_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Configure the chart_frame grid for resizing
chart_frame.grid_columnconfigure(0, weight=1)
chart_frame.grid_columnconfigure(1, weight=1)
chart_frame.grid_columnconfigure(2, weight=1)

tk.Label(chart_frame, text="16:9").grid(row=0, column=0, sticky="nsew")
tk.Label(chart_frame, text="Width (cm)").grid(row=0, column=1, sticky="nsew")
tk.Label(chart_frame, text="Height (cm)").grid(row=0, column=2, sticky="nsew")

chart_169_width = tk.Entry(chart_frame)
chart_169_width.grid(row=1, column=1, sticky="nsew")
chart_169_width.insert(0, "146")

chart_169_height = tk.Entry(chart_frame)
chart_169_height.grid(row=1, column=2, sticky="nsew")
chart_169_height.insert(0, "80")

tk.Label(chart_frame, text="4:3").grid(row=2, column=0, sticky="nsew")

chart_43_width = tk.Entry(chart_frame)
chart_43_width.grid(row=3, column=1, sticky="nsew")
chart_43_width.insert(0, "106.6")

chart_43_height = tk.Entry(chart_frame)
chart_43_height.grid(row=3, column=2, sticky="nsew")
chart_43_height.insert(0, "80")

# Add Measurement Section
measurement_frame = tk.LabelFrame(root, text="Add Measurement", padx=10, pady=10)
measurement_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Configure the measurement_frame grid for resizing
measurement_frame.grid_columnconfigure(0, weight=1)
measurement_frame.grid_columnconfigure(1, weight=1)

device_label = tk.Label(measurement_frame, text="Device")
device_label.grid(row=0, column=0, sticky="nsew")
device_entry = tk.Entry(measurement_frame)
device_entry.grid(row=0, column=1, sticky="nsew")

camera_label = tk.Label(measurement_frame, text="Camera")
camera_label.grid(row=1, column=0, sticky="nsew")
camera_entry = tk.Entry(measurement_frame)
camera_entry.grid(row=1, column=1, sticky="nsew")

mode_label = tk.Label(measurement_frame, text="Mode")
mode_label.grid(row=2, column=0, sticky="nsew")
mode_entry = tk.Entry(measurement_frame)
mode_entry.grid(row=2, column=1, sticky="nsew")

resolution_label = tk.Label(measurement_frame, text="Resolution")
resolution_label.grid(row=3, column=0, sticky="nsew")
resolution_entry = tk.Entry(measurement_frame)
resolution_entry.grid(row=3, column=1, sticky="nsew")

distance_label = tk.Label(measurement_frame, text="Distance to the chart")
distance_label.grid(row=4, column=0, sticky="nsew")
distance_entry = tk.Entry(measurement_frame)
distance_entry.grid(row=4, column=1, sticky="nsew")

aspect_ratio_label = tk.Label(measurement_frame, text="Aspect Ratio")
aspect_ratio_label.grid(row=5, column=0, sticky="nsew")
aspect_ratio_var = StringVar(value="option")
aspect_ratio_menu = OptionMenu(measurement_frame, aspect_ratio_var, "16:9", "4:3")
aspect_ratio_menu.grid(row=5, column=1, sticky="nsew")

# Load the information icon
info_image = Image.open("info_icon.png")
info_image = info_image.resize((20, 20), Image.Resampling.LANCZOS)
info_icon = ImageTk.PhotoImage(info_image)

# Create a label for the information icon
info_label = tk.Label(measurement_frame, image=info_icon)
info_label.grid(row=0, column=2, rowspan=2, sticky="e")

# Example of how the tooltip should look
tooltip_text = "Example:\nDevice: S23U \nCamera: W\nMode: photo\nResolution: 12MP\nDistance: 80 cm"

# Attach the tooltip to the information icon
create_tooltip(info_label, tooltip_text)

# List Box to Display Added Measurements
listbox = Listbox(root, width=50)
listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Configure the listbox to expand with the window
root.grid_rowconfigure(1, weight=2)

# Function to Add Measurement to the List and Clear Fields
def add_to_list():
    # Trim input strings and check for empty fields
    device = device_entry.get().replace(" ", "").upper()
    camera = camera_entry.get().replace(" ", "").upper()
    mode = mode_entry.get().replace(" ", "")
    resolution = resolution_entry.get().replace(" ", "").upper()
    distance = distance_entry.get().replace(" ", "")

    # Check if any input field is empty
    if not device or not camera or not mode or not resolution or not distance:
        messagebox.showerror("Input Error", "All fields must be filled in.")
        return
    
    # Validate that distance can be converted to a float
    try:
        float(distance)
    except ValueError:
        messagebox.showerror("Input Error", "Distance must be a numeric value.")
        return

    # Add the measurement string to the listbox
    measurement = f"{device}_{camera}_{mode}_{resolution}_{aspect_ratio_var.get()}_{distance}"
    listbox.insert(END, measurement)
    
    # Clear the input fields except for "Device"
    camera_entry.delete(0, END)
    mode_entry.delete(0, END)
    resolution_entry.delete(0, END)
    distance_entry.delete(0, END)
    aspect_ratio_var.set("16:9")  # Reset the aspect ratio to default

# Function to Delete Selected Item
def delete_selected_item():
    selected_item_index = listbox.curselection()
    if selected_item_index:
        listbox.delete(selected_item_index)

# Create a Context Menu
context_menu = Menu(root, tearoff=0)
context_menu.add_command(label="Delete", command=delete_selected_item)

# Function to Show the Context Menu on Right-Click
def show_context_menu(event):
    selected_item_index = listbox.curselection()
    if selected_item_index:
        context_menu.post(event.x_root, event.y_root)

# Bind right-click to show context menu
listbox.bind("<Button-3>", show_context_menu)

# Add to List Button
add_button = tk.Button(measurement_frame, text="Add to list", command=add_to_list)
add_button.grid(row=6, column=1, pady=10, sticky="nsew")

# Process Button - Calls process_measurements from the fov_processing module
process_button = tk.Button(root, text="Process", command=lambda: process_measurements(listbox, chart_169_width, chart_169_height, chart_43_width, chart_43_height))
process_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")

# Configure the root grid for the process button row
root.grid_rowconfigure(2, weight=1)

# Start the GUI event loop
root.mainloop()
