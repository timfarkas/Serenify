import tkinter as tk
import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sessions import Session
from database.database import Database,MHWPReview
from sessions import Session
from addfeature.globaldb import global_db
global global_db
db=global_db

def openrating():
    sess = Session()
    sess.open()
    userID = sess.getId()
    root = tk.Tk()
    root.title("Patient info")
    mhwprelation = db.getRelation('Allocation').getRowsWhereEqual('patient_id',userID)
    MHWPID=mhwprelation[0][3]
    mhwpdata=db.getRelation('User').getRowsWhereEqual('user_id',MHWPID)
    username = str(mhwpdata[0][4]) + ' ' + str(mhwpdata[0][5])
    specialization = str(mhwpdata[0][-2])
    email = mhwpdata[0][2]

    def submit_review():
        ratingscore = rating_entry.get()  # Get the input from the entry box
        reviewcomment = input_box.get("1.0", tk.END).strip()
        reviewlist=db.getRelation('MHWPReview')
        mhwpidreview=reviewlist.getRowsWhereEqual('mhwp_id', MHWPID)
        reviewid=None
        for i in mhwpidreview:
            if userID==i[1]:
                reviewid=i[0]
        if reviewid:
            reviewlist.editFieldInRow(reviewid, "reviewscore", int(ratingscore))
            reviewlist.editFieldInRow(reviewid, "reviewcomment",reviewcomment)
            print("review updated")
        else:
            newreviewentry = MHWPReview(
                patient_id=userID,
                mhwp_id=MHWPID,
                reviewscore= int(ratingscore),
                reviewcomment=reviewcomment,
                timestamp=datetime.datetime.now()
            )
            db.insert_review_entry(newreviewentry)
            print("new review created")


        # if user_input.strip():  # Check if the input is not empty
        #     print(f"User Review: {user_input}")  # Display the input (you can save or process it)
        #     input_box.delete(0, tk.END)  # Clear the entry box
        # else:
        #     print("No input provided!")

    # H1 equivalent
    h1_label = tk.Label(root, text="MHWP Review", font=("Arial", 24, "bold"),width=20)
    h1_label.pack()

    fieldset = tk.LabelFrame(root, text="MHWP Information", padx=10, pady=10)
    fieldset.pack(padx=10, pady=10)

    nam_label = tk.Label(fieldset, text="Name: "+username,width=25)
    nam_label.grid(row=0, column=0)
    spe_label = tk.Label(fieldset, text="Specialization: "+specialization)
    spe_label.grid(row=1, column=0)
    ema_label = tk.Label(fieldset, text="Email: "+email)
    ema_label.grid(row=2, column=0)
    #
    # age_label = tk.Label(text="Email:")
    # age_label.grid(row=2, column=0)
    # age_entry = tk.Entry()
    # age_entry.grid(row=2, column=1)

    fieldset2 = tk.LabelFrame(root, text="Rating on MHWP (Scale 1-5):", padx=10, pady=10)
    fieldset2.pack(padx=10, pady=10)
    rating_label = tk.Label(fieldset2,text="Rating")
    rating_label.grid(row=0,column=0)
    rating_entry = tk.Entry(fieldset2)
    rating_entry.grid(row=0,column=1)

    input_box = tk.Text(root, width=30, height=5, font=('Arial', 12), wrap=tk.WORD)
    input_box.pack(padx=10, pady=(0, 10))

    button = tk.Button(root, text="Submit my review", command=submit_review)
    button.pack()

    def on_close():
        # db.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    openrating()