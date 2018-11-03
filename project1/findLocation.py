import sqlite3

conn = None
cur = None
result = None
driver = None

def findLocation(keyword):
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
    #print keys
    '''
    names = tuple(map(lambda x: x[0], cur.description))
    print(names)
    '''

    #get all the matches
    locations = cur.fetchall()
    if len(locations) == 0:
        print('no results found')
        return ''
    #print
    for i in range(0, len(locations), 5):
        if len(locations) <= i+5:
            for j in range(i, len(locations)):
                print(locations[j])
            selection = input('select location(1~{0}) or ''q'' to quit:'.format(len(locations)-i))
            if selection == 'q':
                return ''
        else:
            for j in range(i, i+5):
                print(locations[j])
            selection = input('select locations(1~5), ''y'' to view more, ''q'' to quit:')
            if selection == 'q':
                return ''
            if selection == 'y':
                continue
            else:
                break
    
    return locations[i+int(selection)-1][0]

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
    result = findLocation(keyword)
    print(result)
    conn.close()

if __name__ == '__main__':
    main()