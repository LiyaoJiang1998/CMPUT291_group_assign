import sqlite3
import re

conn = None
cur = None
result = None
driver = None

'''
insert enroute
inputs:
    rno: ride number
    enroute: a set containing enroute lcodes
    conn: connestion to db
'''
def insertEnroute(rno, enroute, conn):
    #assert type(rno) is IntType, 'rno is not integer'
    #assert type(enroute) is SetType,
    cur = conn.cursor()
    insert = '''
                INSERT INTO enroute VALUES (?, ?);
             '''
    for lcode in enroute:
        tup = tuple([rno, lcode])
        cur.execute(insert, tup)
    
    
    return



'''
insert offer into rides
input:
    final: a tuple containing all the information to be inserted
    conn: connection to db
'''
def insertRide(final, conn):
    cur = conn.cursor()
    cur.execute('INSERT INTO rides VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);', final)

    return


'''
get a unique rno, done through adding 1 to max of existing rno
'''
def getUniqueRno(conn):
    cur = conn.cursor()
    findmaxrno = '''
                    SELECT coalesce(max(rno), 0)
                    FROM rides
                 '''
    cur.execute(findmaxrno)
    result = cur.fetchall()
    return result[0][0]+1

'''
checks if car is valid
returns True or False
'''
def carValid(carNo, email, conn):
    cur = conn.cursor()
    findcar = '''
                SELECT *
                FROM cars
                WHERE cno = {0}
                AND owner = '{1}'
              '''.format(carNo, email)
    cur.execute(findcar)
    result = cur.fetchall()
    if len(result) == 1:
        return True
    else:
        return False


#function to find locations based on keyword
#requires a cursor input
def locationSearch(keyword, conn):
    #global conn, cur
    cur = conn.cursor()
    #find 
    findLoc = '''
                SELECT *
                FROM locations
                WHERE lcode = '{0}'
                OR city like '%{0}%'
                OR prov like '%{0}%'
                OR address like '%{0}%'
                COLLATE NOCASES;
              '''.format(keyword)
    cur.execute(findLoc)

    #get all the matches and return
    return cur.fetchall()

'''
given the query results, display 5 at a time and promt selection

inputs:
    results: a list of tuples containing query results
    infoIndex: index of desired item in tuple to be returned

outputs:
    '': if no results were found or user pressed q
    item: key of item selected by user
'''
def displayAndSelect(results, infoIndex):
    if len(results) == 0:
        print('no results found')
        return ''
    #print
    for i in range(0, len(results), 5):
        if len(results) <= i+5:
            for j in range(i, len(results)):
                print(results[j])
            while 1: #promtinput
                selection = input('select options: 1-{0} or ''q'' to quit:'.format(len(results)-i))
                if selection == 'q':
                    return ''
                if re.match('^[1-{0}]$'.format(len(results)-i), selection):
                    break
                print('invalid selection')
        
        else:
            for j in range(i, i+5):
                print(results[j])
            while 1:
                selection = input('select options: 1-5, ''y'' to view more, ''q'' to quit:')
                if selection == 'q':
                    return ''
                if re.match('^[1-5y]$', selection):
                    break
                print('invalid selection')
            if selection == 'y':
                continue
            else: break
                
    return results[i+int(selection)-1][infoIndex]

    #display search results
    '''
    if len(locations) < 5:
        for row in locations:
            print(row)
        selection = input('select location(1~{0}) or ''q'' to quit search or ''a'' to search again:'.format(len(locations)))
        if selection == 'q':
            return
    '''

    return

def main():
    global conn, cur
    path = "./test.db"
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    
    rno = getUniqueRno(conn)
    print(rno)
    
    '''
    keyword = input('keyword: ')
    result = displayAndSelect(locationSearch(keyword, conn), 0)
    print(result)
    '''
    '''
    email = 'joe@gmail.com'
    print(carValid(9, email, conn))
    '''
    conn.close()

if __name__ == '__main__':
    main()