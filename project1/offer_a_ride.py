import sqlite3
import re
import findLocation

conn = None
cur = None
result = None
driver = None

#get source location
def getSource():
    keyword = input('source location keyword:')
    findLocation.displayAndSelect(locationSearch(keyword), 0)
    
    return

#get destination
def getDestination():

    return

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
def getOffer():
    #prompt user input
    print('Input ride offer in the following format')
    print('(quit) to exit offer posting')
    print("(date, number of seats offered, price per seat, luggage description)")
        
    while(1):
        info = input('ride offer: ')
        if (re.match("^\\(quit\\)$", info)):
            return
        
        if (not checkValid(info[1:-1].split(', '))):
            continue
        
        #get sourcelocation
        getSource()

        #get destination
        print('input destination location keyword')
        getDestination()

        #get carnumber
        print('input car number(optional)')
        getCarNo()

        #get enroute
        print('input enroute locations(optional)')
        getEnroute()
        
        

def main():
    #assert(type(conn) == sqlite3.Connection)
    global conn, cur, result
    path = "./test.db"
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    getOffer()
    conn.close()


if __name__ == "__main__":
    main()