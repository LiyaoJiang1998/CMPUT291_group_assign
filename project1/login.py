import sqlite3
import re
import getpass

user = ""

def login(conn):
    global user
    c = conn.cursor()
    print("Welcome to our system! Please login first.")
    # log in or create new account
    while True:
        isAcc = input("Do you have an account? Please enter y if have and n if not or q to quit:")
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
        elif isAcc == "q":
            return False
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
        check = checkUserNameAndPassword(conn, userName, password)
        if check is False:
            continue
        else:
            user = check
            return True

def checkUserNameAndPassword(conn, userName, password):
    c = conn.cursor()
    # check if user name and password is valid
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", userName) and re.match("^[A-Za-z0-9_]*$", password):
        # check if account exists
        c.execute('SELECT * FROM members WHERE email=? and pwd=?;' , (userName, password))
        row = c.fetchone()
        if row is None:
            print("User name does not exist or password is incorrect. Please try again")
            return False
        # if exists
        else:
            print("Account " + userName + " is logged in")
            # print the messages
            showUnreadMessage(conn, userName)
            return userName
    else:
        print("Invalid user name or password, pleae try again")
        return False

def showUnreadMessage(conn, userName):
    c = conn.cursor()
    c.execute('SELECT msgTimestamp, sender, content, rno from inbox where email=? and seen=?;', (userName, 'n'))
    messages = c.fetchall()
    tmp = 1
    for message in messages:
        print("Message" + str(tmp) + ":")
        print("time: " + message[0] + " sender " + message[1] + " content: " + message[2] + " rno " + str(message[3]))
        c.execute('UPDATE inbox set seen=? where msgTimestamp=? and email=?;', ('y', message[0], userName))
        conn.commit()
        tmp += 1

def signup(conn):
    global user
    c = conn.cursor()
    while True:
        userName = signupUserName(conn)
        if userName is True:
            return False
        elif userName is False:
            continue
        else:
            break
    while True:
        password = signupPwd(conn)
        if password is False:
            continue
        else:
            break
    while True:
        name = signupName(conn)
        if name is False:
            continue
        else:
            break
    while True:
        phone = signupPhone(conn)
        if phone is False:
            continue
        else:
            break
    c.execute('INSERT into members values(?, ?, ?, ?);', (userName, name, phone, password))
    conn.commit()
    user = userName
    print("Account created!")
    return True

def signupUserName(conn):
    c = conn.cursor()
    # check the valid user name
    print("if you want to go back to the last screen, enter (quit)")
    userName = input("Please enter your user name (email): ")
    if re.match("^\\(quit\\)$", userName):
        return True
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", userName):
        # check if the user name already exists
        c.execute('SELECT email FROM members WHERE email=?;' , (userName,))
        row = c.fetchone()
        if row is None:
            return userName
        else:
            print("User name already exists. Please use another email.")
    else:
        print("invalid user name, please enter a valid email address")
    return False

def signupPwd(conn):
    c = conn.cursor()
    # check valid password
    password = getpass.getpass("Please enter your password:")
    if re.match("^[A-Za-z0-9_]*$", password):
        return password
    else:
        print("Invalid password format, please only use letter, number and undersccore")
        return False

def signupName(conn):
    c = conn.cursor()
    name = input("Please enter your name: ")
    if re.match("^[ A-Za-z]*$", name):
        return name
    else:
        print("Invalid name style")
        return False

def signupPhone(conn):
    c = conn.cursor()
    phone = input("Please enter your phone number: ")
    if re.match("^[0-9]*$", phone):
        return phone
    else:
        print("Invalid phone number.")
        return False