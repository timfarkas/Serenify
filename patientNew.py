import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Sample tkinter App")

# Create a button widget
button = tk.Button(root, text="Click Me!")
button.pack()

# H1 equivalent
h1_label = tk.Label(root, text="Heading ", font=("Arial", 24, "bold"))
h1_label.pack()

# H2 equivalent
h2_label = tk.Label(root, text="Heading 2", font=("Arial", 18, "bold"))
h2_label.pack()

# H3 equivalent
h3_label = tk.Label(root, text="Heading 3", font=("Arial", 14, "bold"))
h3_label.pack()

# Run the application
root.mainloop()
