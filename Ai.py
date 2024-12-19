# Import necessary libraries
from owlready2 import *
import tkinter as tk
from tkinter import messagebox

# Load OWL Ontology and Run Pellet Reasoner
ontology_path = "geometry.owl"  # Replace with the path to your OWL file
onto = get_ontology(ontology_path).load()

with onto:
    sync_reasoner_pellet(infer_property_values=True)  # Run Pellet Reasoner

# Initialize Tkinter root window
root = tk.Tk()
root.title("Intelligent Tutoring System for Geometry")
root.geometry("600x500")

# Function to calculate area based on user inputs
def calculate_area():
    shape = shape_var.get()
    result_label.config(text="")
    
    try:
        if shape == "Triangle":
            base = float(entry_base.get())
            height = float(entry_height.get())
            area = 0.5 * base * height
            result_label.config(text=f"Area of Triangle: {area:.2f} units²\nFormula: 0.5 × base × height")
            
        elif shape == "Square":
            side = float(entry_side.get())
            area = side ** 2
            result_label.config(text=f"Area of Square: {area:.2f} units²\nFormula: side²")
            
        elif shape == "Circle":
            radius = float(entry_radius.get())
            area = 3.1416 * (radius ** 2)
            result_label.config(text=f"Area of Circle: {area:.2f} units²\nFormula: π × radius²")
            
        else:
            result_label.config(text="Please select a shape to calculate area.")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Function to query ontology and display shape details
def query_ontology():
    selected_shape = shape_var.get()
    output = ""

    if selected_shape == "Triangle":
        for triangle in onto.Triangle.instances():
            base = triangle.hasBase[0] if triangle.hasBase else "N/A"
            height = triangle.hasHeight[0] if triangle.hasHeight else "N/A"
            area = triangle.calculateArea[0] if triangle.calculateArea else "N/A"
            output += f"Triangle -> Base: {base}, Height: {height}, Area: {area}\n"

    elif selected_shape == "Square":
        for square in onto.Square.instances():
            side = square.hasSide[0] if square.hasSide else "N/A"
            area = square.calculateArea[0] if square.calculateArea else "N/A"
            output += f"Square -> Side: {side}, Area: {area}\n"

    elif selected_shape == "Circle":
        for circle in onto.Circle.instances():
            radius = circle.hasRadius[0] if circle.hasRadius else "N/A"
            area = circle.calculateArea[0] if circle.calculateArea else "N/A"
            output += f"Circle -> Radius: {radius}, Area: {area}\n"

    else:
        output = "Please select a shape to query the ontology."

    result_label.config(text=output)

# Function to toggle input fields based on shape selection
def toggle_inputs(*args):
    shape = shape_var.get()
    entry_base.pack_forget()
    entry_height.pack_forget()
    entry_side.pack_forget()
    entry_radius.pack_forget()
    base_label.pack_forget()
    height_label.pack_forget()
    side_label.pack_forget()
    radius_label.pack_forget()
    
    if shape == "Triangle":
        base_label.pack()
        entry_base.pack()
        height_label.pack()
        entry_height.pack()
    elif shape == "Square":
        side_label.pack()
        entry_side.pack()
    elif shape == "Circle":
        radius_label.pack()
        entry_radius.pack()

# Shape selection dropdown
shape_var = tk.StringVar()
shape_var.trace_add('write', toggle_inputs)

shape_label = tk.Label(root, text="Select Shape:")
shape_label.pack()

shape_dropdown = tk.OptionMenu(root, shape_var, "Triangle", "Square", "Circle")
shape_dropdown.pack()

# Input fields for dimensions
base_label = tk.Label(root, text="Base:")
entry_base = tk.Entry(root)

height_label = tk.Label(root, text="Height:")
entry_height = tk.Entry(root)

side_label = tk.Label(root, text="Side:")
entry_side = tk.Entry(root)

radius_label = tk.Label(root, text="Radius:")
entry_radius = tk.Entry(root)

# Buttons
calc_button = tk.Button(root, text="Calculate Area", command=calculate_area)
calc_button.pack()

query_button = tk.Button(root, text="Query Ontology", command=query_ontology)
query_button.pack()

# Result display
result_label = tk.Label(root, text="", font=("Arial", 12), fg="green")
result_label.pack()

# Start the GUI main loop
root.mainloop()
