from bsddb3 import db
import re


def exaTermQuery(term):
    database = db.DB()
    database.open("./outputs/te.idx")
    curs = database.cursor()
    aids = []
    aid = curs.set(term.lower().encode("utf-8"))

    while(aid != None):
        aids.append(aid[1])
        aid = curs.next_dup()
    curs.close()
    database.close()
    return aids

def nonExaTermQuery(term):
    database = db.DB()
    database.open("./outputs/te.idx")
    curs = database.cursor()
    aids = []
    aid = curs.set_range(term.lower().encode("utf-8"))

    while (aid is not None):
        if(str(aid[0].decode("utf-8")[0:len(term)]) > term):
            break
        aids.append(aid[1])
        aid = curs.next()
    curs.close()
    database.close()
    return aids

def infoQuery(info, aids):
    resultId = []
    database = db.DB()
    database.open("./outputs/ad.idx")
    for aid in aids:
        if info[0] == "location":
            name = "loc"
        else:
            name = info[0]
        result = database.get(aid)
        m = re.search('<{0}>.+<\/{0}>'.format(name), result.decode("utf-8"))
        value = m.group(0).replace('<{0}>'.format(name),'').replace('</{0}>'.format(name),'').lower()
        if info[2] == value:
            resultId.append(aid)
    database.close()
    return resultId

def getAllAids():
    database = db.DB()
    database.open("./outputs/ad.idx")
    curs = database.cursor()
    iter = curs.first()
    aids = []
    while (iter):
        aids.append(iter[0])
        iter = curs.next()
    return aids

def getRecords(aids):
    database = db.DB()
    database.open("./outputs/ad.idx")
    curs = database.cursor()
    records = []
    for aid in aids:
        records.append((curs.set(aid)[0].decode("utf-8"), curs.set(aid)[1].decode("utf-8")))

    curs.close()
    database.close()
    return records

def main():
    term = input("")
    result = nonExaTermQuery(term)
    print(result)

if __name__ == "__main__":
    main()
