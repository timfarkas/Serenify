import tkinter as tk

root = tk.Tk()

# H1 equivalent
h1_label = tk.Label(root, text="Heading 1", font=("Arial", 24, "bold"))
h1_label.pack()

# H2 equivalent
h2_label = tk.Label(root, text="Heading 2", font=("Arial", 18, "bold"))
h2_label.pack()


# p tag equivalent
paragraph = tk.Label(root, text="This is a paragraph of text. It is wrapped automatically to fit the window size.",wraplength=300)  # Wrap text after 300 pixels
paragraph.pack()


# button 
button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack()


# input field
entry = tk.Entry(root)
entry.pack() # to get the text entered use 'entry.get()'


# fieldset equivalent
fieldset = tk.LabelFrame(root, text="Personal Information", padx=10, pady=10)
fieldset.pack(padx=10, pady=10)

name_label = tk.Label(fieldset, text="Name:")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(fieldset)
name_entry.grid(row=0, column=1) 

age_label = tk.Label(fieldset, text="Age:")
age_label.grid(row=1, column=0)
age_entry = tk.Entry(fieldset)
age_entry.grid(row=1, column=1) # note the change in number change in rows


# display an image
image = PhotoImage(file="path_to_image.png")  # Image file should be a .gif or .png
image_label = tk.Label(root, image=image)
image_label.pack()


# list equivalent
listbox = tk.Listbox(root)
items = ["Item 1", "Item 2", "Item 3"]
for item in items:
    listbox.insert(tk.END, item)
listbox.pack()


# dropdown menu equivalent
combo = ttk.Combobox(root, values=["Option 1", "Option 2", "Option 3"])
combo.set("Select an option")  # Default text
combo.pack()


# checkbox equivalent
var = tk.IntVar()  # Variable to store checkbox state (0 or 1)
checkbox = tk.Checkbutton(root, text="I agree", variable=var)
checkbox.pack()


# radio button equivalent
radio_var = tk.StringVar()

radio1 = tk.Radiobutton(root, text="Option A", variable=radio_var, value="A")
radio2 = tk.Radiobutton(root, text="Option B", variable=radio_var, value="B")
radio1.pack()
radio2.pack()


# form equivalent
form = tk.Frame(root)
form.pack()

tk.Label(form, text="Username:").grid(row=0, column=0)
username_entry = tk.Entry(form)
username_entry.grid(row=0, column=1)

tk.Label(form, text="Password:").grid(row=1, column=0)
password_entry = tk.Entry(form, show="*")  
password_entry.grid(row=1, column=1)

root.mainloop()