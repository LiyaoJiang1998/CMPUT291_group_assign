import sqlite3
import re

# Hongru Qi
# search user's requests
def userSearch(conn, email):
    c = conn.cursor()
    c.execute('SELECT * from requests where email=?;', (email,))
    requests = c.fetchall()
    makeSelection(conn, email, requests)

# delete request
def delete(conn, rid, email):
    c = conn.cursor()
    c.execute('SELECT * from requests where rid=? and email=?;', (rid, email))
    request = c.fetchone()
    if request is None:
        print("the request is not posted by you and you cannot delete it")
    else:
        c.execute('DELETE from requests where rid=? and email=?;', (rid,email))
        conn.commit()

# search requests by lcode
def searchByLcode(conn, email, lcode):
    c = conn.cursor()
    c.execute('SELECT * from requests where pickup=?;', (lcode,))
    requests = c.fetchall()
    makeSelection(conn, email, requests)

# search requests by city
def searchByCity(conn, email, city):
    c = conn.cursor()
    c.execute('SELECT * from requests where pickup in (SELECT lcode from locations where city=? COLLATE NOCASE);', (city,))
    requests = c.fetchall()
    makeSelection(conn, email, requests)

# send message to user who posted requests
def sendMessage(conn, email, receiver, content):
    c = conn.cursor()
    c.execute('INSERT into inbox (email, msgTimestamp, sender, content, seen) values (?, datetime("now"), ?, ?, ?);', (receiver,  email, content, 'n'))
    conn.commit()

# print the searched requests
def makeSelection(conn, email, requests):
    while True:
        selection = displayAndSelect(requests)
        # quit
        if selection is True:
            return
        # no results found
        elif selection is "":
            return
        # send message
        else:
            content = input("Please enter the massage content or q to quit: ")
            if content == "q":
                return
            sendMessage(conn, email, selection[1], content)
            ano = input("Message sent, enter y to send another message or q to quit: ")
            if ano == "y":
                continue
            else:
                break
            return

# display the searched results and make selections to send message
def displayAndSelect(results):
    if len(results) == 0:
        print('no results found')
        return ''
    #print
    print("request ID | request date | pickup location | dropoff location | amount")
    for i in range(0, len(results), 5):
        # more than 5, only print 5
        if len(results) <= i+5:
            for j in range(i, len(results)):
                print(results[j])
            while 1: #promtinput
                selection = input('select one to send message (options: 1-{0}) or ''q'' to quit:'.format(len(results)-i))
                if selection == 'q':
                    return True
                if re.match('^[1-{0}]$'.format(len(results)-i), selection):
                    break
                print('invalid selection')
        # less than 5, print all
        else:
            for j in range(i, i+5):
                print(results[j])
            while 1:
                selection = input('select one to send message (options: 1-5), ''y'' to view more, ''q'' to quit:')
                if selection == 'q':
                    return True
                if re.match('^[1-5y]$', selection):
                    break
                print('invalid selection')
            if selection == 'y':
                continue
            else: break

    return results[i+int(selection)-1]

# search requests (main search operation)
def search(conn, email):
    searchOp = input("Enter 1 to search your requests and 2 to search by location or q to go to the previous screen: ")
    # search user's requests
    if searchOp == '1':
        userSearch(conn, email)
    # search by location
    elif searchOp == '2':
        isLcode = input("Enter 1 to search by lcode or 2 by city: ")
        # seach by lcode
        if isLcode == '1':
            lcode = input("Please enter the lcode: ")
            searchByLcode(conn, email, lcode)
        # search by city
        elif isLcode == '2':
            city = input("Please enter the city: ")
            searchByCity(conn, email, city)
        else:
            print("Invalid input")
    # quit
    elif searchOp == "q":
        return False
    else:
        print("Invalid input")


# get the user's operation
def getOperation(conn, email):
    print("Do you want to search or delete or send message?")
    print("Enter q to go back to the previous screen")
    op = input("Enter 1 for search, 2 for delete: ")
    # seach requests
    if op == '1':
        while True:
            result = search(conn, email)
            if result is False:
                break
    # delete requests
    elif op == '2':
        while True:
            rid = input("Please enter the request ID of the request to delete or q to go to the previous screen: ")
            if rid == "q":
                break
            delete(conn, rid, email)
    # quit
    elif op == 'q':
        return False
    else:
        print("Invalid input")

# main opeational function
def searchAndDelete(conn, email):
    while True:
        command = getOperation(conn, email)
        if command == False:
            break
