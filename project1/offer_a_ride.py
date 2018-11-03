import sqlite3
import re
from queries import *

conn = None
cur = None
result = None
driver = None

#get source location
def getSource():
    global conn, cur
    keyword = input('input source location keyword: ')

    return displayAndSelect(locationSearch(keyword, cur), 0)

#get destination
def getDestination():
    global conn, cur
    keyword = input('input destination location keyword: ')

    return displayAndSelect(locationSearch(keyword, cur), 0)

#get car number
def getCarNo():

    return

#get enroute
def getEnroute():

    return

#find location


#checks if user input is valid (excluding locations)
def checkValid(result):
    #make sure length is 4
    if (len(result) != 4):
        print('invalid number of arguments')
        return False

    #match date, format 'YYYY-MM-DD'
    if (re.match('[1-9][0-9]{3}-(0[1-9]|1[0-2])-[0-9]{2}', result[0]) == None):
        print('invalid date')
        return False

    #match seats
    if (re.match('[1-9][0-9]*', result[1]) == None):
        print('invalid seats')
        return False

    #match price per seat
    if (re.match('[1-9][0-9]*', result[2]) == None):
        print('invalid seats')
        return False

    #match luggage description
    if (re.match('[a-zA-Z]{1,10}', result[3]) == None):
        print('invalid luggage')
        return False
    
    return True

    

#get user input
#requires user email
def postOffer(email):
    #global result
    #prompt user input
    print('Input ride offer in the following format')
    print('(quit) to exit offer posting')
    print("(date, number of seats offered, price per seat, luggage description)")
        
    while(1):
        info = input('ride offer: ')
        if (re.match("^\\(quit\\)$", info)):
            return
        info = info[1:-1].split(', ')
        if (not checkValid(info)):
            continue
        
        #get sourcelocation
        source = getSource()
        if source == '': 
            print('no source location input, try again')
            continue
        info += [source]

        #get destination
        destination = getDestination()
        if destination == '': 
            print('no destination location input, try again')
            continue
        info += [destination]

        #get carnumber
        print('input car number(optional)')
        getCarNo()

        #get enroute
        print('input enroute locations(optional)')
        getEnroute()

        print(info)
        
        

def main():
    #assert(type(conn) == sqlite3.Connection)
    global conn, cur, result
    path = "./test.db"
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    email = 'joe@gmail.com'
    postOffer(email)
    conn.close()


if __name__ == "__main__":
    main()