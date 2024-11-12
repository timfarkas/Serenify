"""A toy project for a study room booking system. To try out, please use username "p1" and password"1"""
"""User Database"""
# User data is structured as a dictionary within a dictionary. The outer dictionary used username as its key, and inner dictionary as its value. The inner dictionary used attributes as its keys, and attribute value as its value.
# With this data structure, if we want to get the age of user p2, we can just use the following function: print(Userdata["p2"]["Age"])."""
# Some initial data for testing purpose
Userdata ={"p1" :{"Password" :"1" ,"Name" :"John" ,"Age" :25 ,"Skilllevel" :5},
          "p2" :{"Password" :"111" ,"Name" :"Tony" ,"Age" :30 ,"Skilllevel" :2},
          "p3" :{"Password" :"qqq" ,"Name" :"Jane" ,"Age" :28 ,"Skilllevel" :4}}

"""A timetable for a week with 7 days and 14 timeslots on each day, including the booking status on each timeslot."""
timelist=[]
timestandard=[str(num).zfill(2) for num in range(7,22)]
for i in range(len(timestandard)-1):
        timelist.append(str(timestandard[i])+"-"+str(timestandard[i+1]))
daylist=["Monday    ","Tuesday   ","Wednesday ","Thursday  ","Friday    ","Saturday  ","Sunday    "]
bookingslot=[["Free "]*len(timelist) for i in range(7)]
sessionlist=["A","B","C","D","E","F","G","H","I","J","K","L","M","N"]
sessionstandard=["  "+i+"  " for i in sessionlist]


""" A function used to display the timetable"""
def printtimetable():
    print("----------------------------------------------------------------------------------------------------------------------------")
    print("<session >", *sessionstandard, "", sep=" | ")
    print("<timeslot>", *timelist, "", sep=" | ")
    print("----------------------------------------------------------------------------------------------------------------------------")
    for i in range(7):
        print(daylist[i], *bookingslot[i], "", sep=" | ")

""" A function used to log in user account"""
def login():
    global loggedin
    global stage
    print("-----------------------")
    print("Welcome to log in")
    print("-----------------------")
    accountname=input("Please enter account name: ")
    accountpassword=input("Please enter password: ")
    if accountname in Userdata:
        if Userdata[accountname]["Password"] == accountpassword:
            print(accountname,"login successful")
            loggedin = accountname  #If logged in successully, the value of the global variable "loggein" will become "username", using to indentify user in following functions.
            stage="1" #If logged in successully, jump to stage 1 (where user can review personal information and make an appointment)
        else:
            print("Wrong password. Please try again.")
    else:
        print("No matching account name. Please try again.")

"""A function used to register a new user and add data to the user database"""
def register():
    print("-----------------------")
    print("Welcome to register")
    print("-----------------------")
    newaccountname=input("Please enter new account name: ")
    newaccountpassword=input("Please enter new password: ")
    if newaccountname in Userdata:
        print("User already exist. Please try again")
    else:
        Userdata[newaccountname]=dict()
        Userdata[newaccountname]["Password"]=newaccountpassword
        newrealname = input("Please enter real name: ")
        newage= input("Please enter age: ")
        newskilllevel = input("Please enter skill level: ")
        Userdata[newaccountname]["Name"]=newrealname
        Userdata[newaccountname]["Age"]=newage
        Userdata[newaccountname]["Skilllevel"]=newskilllevel
        print ("Registration successful")

"""The offical starting point of program"""
loggedin = None #No user is logged in at the beginning
stage = "0" #The program starts with the initial stage - 0
#The main code is structed as while-loops within while-loop. The reason to use loops is to make sure we can always go back to previous stages during the running process. To control the process, stage codes ("0","1","2","-1") are used, so that the program will always go to a specific stage once a stage code is given.
while  stage =="0":
    print("[1] Log in \n[2] Sign up \n[0] Exit")
    action = input("Please choose action:")
    if action=="1":
        login()  #If logged in successully, jump to stage 1
    elif action=="2":
        register()
    elif action == "0":
        stage = "-1" #With a stage code of "-1", the program will go directly to the end and stop, since no while loop is going to be triggered.

    while stage =="1":
        print("[1] Show information \n[2] Enter booking page \n[9] Return \n[0] Exit")
        action = input("Please choose action:")
        if action == "1":
            print("-----------------------")
            print("Name: ",Userdata[loggedin]["Name"])
            print("Age: ", Userdata[loggedin]["Age"])
            print("Skilllevel: ", Userdata[loggedin]["Age"])
            print("-----------------------")
            stage = "1"
        elif action == "2":
            stage="2"
        elif action == "9":
            stage= str(int(stage)-1)  #Go back to a previous stage by deducting the stage code by 1.
        elif action == "0":
            stage="-1"

        while stage=="2":
            try:
                printtimetable()
                print(" ")
                print("[1] Make an appointment \n[2] Cancel an appointment \n[9] Return \n[0] Exit")
                action = input("Please choose action:")
                if action=="1":
                    selectday=input("Please choose the day [1-7]")
                    selectsession = input("Please choose the session [A-N]")
                    if bookingslot[int(selectday)-1][sessionlist.index(selectsession)]=="Free ":
                        bookingslot[int(selectday)-1][sessionlist.index(selectsession)] = "Taken"
                        print("Book successful at","Day:",daylist[int(selectday)-1],"Time:",sessionstandard[sessionlist.index(selectsession)])
                    else:
                        print("Session is already taken. Please try again")
                elif action == "2":
                    selectday = input("Please choose the day [1-7]")
                    selectsession = input("Please choose the session [A-N]")
                    if bookingslot[int(selectday) - 1][sessionlist.index(selectsession)] == "Taken":
                        bookingslot[int(selectday) - 1][sessionlist.index(selectsession)] = "Free "
                        print("Cancel successful at","Day:", daylist[int(selectday) - 1],"Time:",
                              timelist[sessionlist.index(selectsession)])
                    else:
                        print("Session is not taken. Cannot cancel.")
                elif action == "9":
                    stage = str(int(stage) - 1)
                elif action == "0":
                        stage = "-1"
            except:
                print("Wrong input. Please try again.")
print("Exit Successful. See you again.")