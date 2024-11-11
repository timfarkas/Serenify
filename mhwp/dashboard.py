import tkinter as tk

root = tk.Tk()
root.title("Patient Dashboard")

# H1 equivalent
h1_label = tk.Label(root, text="Knowledge", font=("Arial", 24, "bold"))
h1_label.pack()

# All patient data and a chart per patient (Matplotlib) with their mood tracking info

    ####### Back button - needs completing #######
    # self.back_button = tk.Button(root, text="Login", command=self.backButton)
    # self.back_button.pack()

    # def backButton(self):
    #     subprocess.Popen(["python3", "mhwpMain.py"])
    #     self.root.destroy()
    
root.mainloop()