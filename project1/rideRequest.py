import sqlite3
import re

def singleSearch(conn, email):
    c = conn.cursor()
    c.execute('SELECT rid, rdate, pickup, dropoff, amount from requests where email=?;', (email,))
    requests = c.fetchall()
    printRequests(requests)

def delete(conn, rid):
    c = conn.cursor()
    c.execute('DELETE from requests where rid=?;', (rid,))

def searchByLcode(conn, lcode):
    c = conn.cursor()
    c.execute('SELECT rid, rdate, pickup, dropoff, amount from requests where pickup=?;', (lcode,))
    requests = c.fetchall()
    printRequests(requests)

def searchByCity(conn, city):
    c = conn.cursor()
    c.execute('SELECT rid, rdate, pickup, dropoff, amount from requests where pickup in (SELECT lcode from locations where city=?);', (city,))
    requests = c.fetchall()
    printRequests(requests)

def sendMessage(conn, myEmail, requestEmail, content):
    c = conn.cursor()
    c.execute('INSERT into inbox (email, msgTimestamp, sender, content, seen) values (?, datetime("now"), ?, ?, ?);', (requestEmail,  myEmail, content, 'n'))
    conn.commit()


def printRequests(requests):
    print("request ID | request date | pickup location | dropoff location | amount")
    for request in requests:
        print(str(request[0]) + " | " + request[1] + " | " + request[2] + " | " + request[3] + " | " + str(request[4]))


def search(conn, email):
    searchOp = input("Enter 1 to search your requests and 2 to search by location: ")
    if searchOp == '1':
        singleSearch(conn, email)
    elif searchOp == '2':
        isLcode = input("Enter 1 to search by lcode or 2 by city: ")
        if isLcode == '1':
            lcode = input("Please enter the lcode: ")
            searchByLcode(conn, lcode)
        elif isLcode == '2':
            city = input("Please enter the city: ")
            searchByCity(conn, city)
        else:
            print("Invalid input")
    else:
        print("Invalid input")



def operation(conn, email):
    print("Do you want to search or delete or send message?")
    print("Enter (quit) to go back to the previous screen")
    op = input("Enter 1 for search, 2 for deleter and 3 for sending message: ")
    if op == '1':
        search(conn, email)
    elif op == '2':
        rid = input("Please enter the rid of the request to delete: ")
        delete(conn, rid)
    elif op == '3':
        requestEmail = input("Send email to: ")
        content = input("Please enter the content: ")
        sendMessage(conn, email, requestEmail, content)
    elif re.match("^\\(quit\\)$", op):
        return True
    else:
        print("Invalid input")
    return False

def searchAndDelete(conn, email):
    while True:
        command = operation(conn, email)
        if command == True:
            break
def main():
    conn = sqlite3.connect('./pro1.db')
    email = '1@1.com'
    searchAndDelete(conn, email)

if __name__ == "__main__":
    main()
