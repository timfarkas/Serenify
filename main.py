from sessions import Session

if __name__ == "__main__":
    ### INITIALIZE SESSION 
    # (do this just once when opening the app)
    session = Session()
    session._initialize()


    ### SET ID AND ROLE (DO THIS AFTER EACH SUCCESSFUL LOGIN)
    session.setId(4)
    session.setRole("MHWP")

    ### SET EXTRA DETAILS, e.g. isDisabled
    session.set("isDisabled", True)

    session.close() ## this saves the session




