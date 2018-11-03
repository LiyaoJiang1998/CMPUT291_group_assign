import sqlite3
import re
import getpass

user = ""

def login(conn):
    c = conn.cursor()
    print("Welcome to our system! Please login first.")
    # log in or create new account
    while True:
        isAcc = input("Do you have an account? Please enter y if have and n if not:")
        # log in
        if isAcc == "y":
            result = log(conn)
            if result is True:
                break
            # create account
        elif isAcc == "n":
            print("Please create your account")
            result = signup(conn)
            if result is True:
                break
        else:
            print("invalid input")
    return user

def log(conn):
    global user
    c = conn.cursor()
    while True:
        print("if you want to go back to the last screen, enter (quit)")
        userName = input("Please enter your user name (email):")
        # check if user wants to quit
        if re.match("^\\(quit\\)$", userName):
            return False
        password = getpass.getpass("Please enter your password:")
        # check if user name and password is valid
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", userName) and re.match("^[A-Za-z0-9_]*$", password):
            # check if account exists
            c.execute('SELECT * FROM members WHERE email=? and pwd=?;' , (userName, password))
            row = c.fetchone()
            if row is None:
                print("User name does not exist or password is incorrect. Please try again")
            # if exists
            else:
                print("Account " + userName + " is logged in")
                user = userName
                # print the messages
                c.execute('SELECT msgTimestamp, sender, content, rno from inbox where email=? and seen=?;', (userName, 'n'))
                messages = c.fetchall()
                tmp = 1
                for message in messages:
                    print("Message" + str(tmp) + ":")
                    print("time: " + message[0] + " sender " + message[1] + " content: " + message[2] + " rno " + str(message[3]))
                    c.execute('UPDATE inbox set seen=? where msgTimestamp=? and email=?;', ('y', message[0], email))
                    conn.commit()
                    tmp += 1
                return True
        else:
            print("Invalid user name or password, pleae try again")

def signup(conn):
    global user
    c = conn.cursor()
    while True:
        # check the valid user name
        print("if you want to go back to the last screen, enter (quit)")
        userName = input("Please enter your user name (email): ")
        if re.match("^\\(quit\\)$", userName):
            return False
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", userName):
            # check if the user name already exists
            c.execute('SELECT email FROM members WHERE email=?;' , (userName,))
            row = c.fetchone()
            if row is None:
                break
            else:
                print("User name already exists. Please use another email.")
        else:
            print("invalid user name, please enter a valid email address")
    while True:
        # check valid password
        password = getpass.getpass("Please enter your password:")
        if re.match("^[A-Za-z0-9_]*$", password):
            break
        else:
            print("Invalid password format, please only use letter, number and undersccore")
    # enter name and phone number
    name = input("Please enter your name: ")
    while True:
        phone = input("Please enter your phone number: ")
        if re.match("^[0-9]*$", phone):
            break
        else:
            print("Invalid phone number.")
    c.execute('INSERT into members values(?, ?, ?, ?);', (userName, name, phone, password))
    conn.commit()
    user = userName
    print("Account created!")
    return True
