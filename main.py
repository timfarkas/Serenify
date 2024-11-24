from database.database import Database


if __name__ == "__main__":
    # Initialize the database
    ## This automatically loads the database from database.pkl, or creates a new one if that file doesn't exist
    db = Database()

    ### print whole contents of loaded database (for testing purposes)
    db.printAll()

    # Save the database state before exiting (IMPORTANT, CHANGES WON'T BE SAVED OTHERWISE)
    db.close()