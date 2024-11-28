from sessions import Session

if __name__ == "__main__":
    ### EXAMPLE OF HOW TO CALL UP THE SESSION 
    
    ## open session
    sess = Session()
    sess.open()

    ## get id and role from session
    userId = sess.getId()
    userRole = sess.getRole()

    ## get any other details
    isDisabled = sess.get("isDisabled")

    print(userId)
    print(userRole)
    print(isDisabled)
    
    ### no need to close the session as long as you're not 
    ### setting extra variables that need to be saved


