import sqlite3
import re

def searchRide(conn, email):
    c = conn.cursor()
    keyword = input("Please enter up to 3 location keywords (seperated by space) or (quit) to quit: ")
    if keyword == "(quit)":
        return False
    keywords = keyword.split()
    findRides = ""

    tmp1 = 0
    if len(keywords) > 1:
        for keyword in keywords:
            tmp = 0
            findRides += "select * from ("
            lcodes = locationSearch(conn, keyword)
            lcodes = [x for subtuples in lcodes for x in subtuples]
            for lcode in lcodes:
                if tmp < len(lcodes) - 1:
                    findRides += (rideSearch(lcode) + " union ")
                else:
                    findRides += rideSearch(lcode)
                tmp += 1

            if tmp1 < len(keywords) - 1:
                findRides += ") intersect "
            else:
                findRides += ")"
            tmp1 += 1
    else:
        lcodes = locationSearch(conn, keywords[0])
        lcodes = [x for subtuples in lcodes for x in subtuples]
        tmp = 0
        for lcode in lcodes:
            if tmp < len(lcodes) - 1:
                findRides += (rideSearch(lcode) + " union ")
            else:
                findRides += rideSearch(lcode) + ";"
            tmp += 1
    print(findRides)
    c.execute(findRides)
    rides = c.fetchall()
    while True:
        selection = displayAndSelect(rides)
        if selection is True:
            break
        if selection is "":
            break
        sendMsg(conn, selection, email)

def mainOp(conn, email):
    while True:
        result = searchRide(conn, email)
        if result is False:
            break


def rideSearch(keyword):
    findRide = '''
                select distinct(r.rno), r.price, r.rdate, r.seats, r.lugDesc, r.src, r.dst, r.driver, r.cno, t1.make, t1.model, t1.year, t1.seats, t1.owner
                from rides r, enroute e
                left outer join (select c.cno, c.make, c.model, c.year, c.seats, c.owner
                from cars c, rides r1, enroute e1 where c.cno = r1.cno
                and r1.cno is not null and (r1.dst = '{0}' or r1.src = '{0}' or (r1.rno = e1.rno and e1.lcode= '{0}'))) t1 on t1.cno = r.cno
                where r.rno = e.rno
                and r.dst = '{0}' or r.src = '{0}' or (r.rno = e.rno and e.lcode= '{0}')
              '''.format(keyword)

    return findRide

def locationSearch(conn, keyword):
    #global conn, cur
    cur = conn.cursor()
    #find
    findLoc = '''
                SELECT lcode
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

def displayAndSelect(results):
    if len(results) == 0:
        print('no results found')
        return ''
    #print
    print("ride no | price | ride date | seats | luggage Description | source | destination | driver | car no | car make | car model | year of car | seats of car | car owner")
    for i in range(0, len(results), 5):
        if len(results) <= i+5:
            for j in range(i, len(results)):
                print(results[j])
            while 1: #promtinput
                selection = input('select options: 1-{0} or ''q'' to quit:'.format(len(results)-i))
                if selection == 'q':
                    return True
                if re.match('^[1-{0}]$'.format(len(results)-i), selection):
                    break
                print('invalid selection')

        else:
            for j in range(i, i+5):
                print(results[j])
            while 1:
                selection = input('select options: 1-5, ''y'' to view more, ''q'' to quit:')
                if selection == 'q':
                    return True
                if re.match('^[1-5y]$', selection):
                    break
                print('invalid selection')
            if selection == 'y':
                continue
            else: break

    return results[i+int(selection)-1]

def sendMsg(conn, selection, email):
    c = conn.cursor()
    msg = input("Please enter your msg or (quit) to go to the previous page: ")
    if msg == "(quit)":
        return
    c.execute('INSERT into inbox values (?, datetime("now", "localtime"), ?, ?, ?, ?);', (selection[7], email, msg, selection[0], 'n'))
    conn.commit()
