import tkinter as tk

root = tk.Tk()
root.title("Patient Dashboard")

# H1 equivalent
h1_label = tk.Label(root, text="Knowledge", font=("Arial", 24, "bold"))
h1_label.pack()

# All patient data and a chart per patient (Matplotlib) with their mood tracking info


root.mainloop()