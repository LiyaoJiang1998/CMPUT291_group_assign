import sqlite3
import re

conn = None
cur = None
result = None
driver = None

#function to find locations based on keyword
def locationSearch(keyword):
    global conn, cur
    #find 
    result = ''
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

#given the query results, display 5 at a time and promt selection
#results: list of tuples containing query results
#infoIndex: index of desired item in tuple to be returned
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
    keyword = input('keyword: ')
    result = displayAndSelect(locationSearch(keyword), 0)
    print(result)
    conn.close()

if __name__ == '__main__':
    main()