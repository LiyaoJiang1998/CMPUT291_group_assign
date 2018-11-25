from bsddb3 import db
import time
import datetime


def str2time(dateStr):
    t = time.mktime(datetime.datetime.strptime(dateStr, "%Y/%m/%d").timetuple())
    return t


def evalDate(operator, dateStr):
    '''
    takes in the operator and the given date String
    perform the search and return the key of the qualified
    entries
    '''
    # convert the yyyy/mm/dd string into time format
    date = str2time(dateStr)
    records = []

    database = db.DB()
    database.open("./outputs/da.idx")
    cur = database.cursor()
    iter = cur.first()
    while iter:
        entryDate = str2time(iter[0].decode("utf-8"))
        if operator == "<":
            if entryDate < date:
                # get the aid
                key = iter[1].decode("utf-8").split(',')[0]
                records.append(key.encode('utf-8'))
        elif operator == ">":
            if entryDate > date:
                # get the aid
                key = iter[1].decode("utf-8").split(',')[0]
                records.append(key.encode('utf-8'))
        elif operator == "<=":
            if entryDate <= date:
                # get the aid
                key = iter[1].decode("utf-8").split(',')[0]
                records.append(key.encode('utf-8'))
        elif operator == ">=":
            if entryDate >= date:
                # get the aid
                key = iter[1].decode("utf-8").split(',')[0]
                records.append(key.encode('utf-8'))
        elif operator == "=":
            if entryDate == date:
                # get the aid
                key = iter[1].decode("utf-8").split(',')[0]
                records.append(key.encode('utf-8'))
        else:
            break
        iter = cur.next()

    cur.close()
    database.close()
    return records


def evalPrice(operator, priceStr):
    '''
    takes in the operator and the given price String
    perform the search and return the key of the qualified
    entries
    '''
    records = []
    price = int(priceStr)

    database = db.DB()
    database.open("./outputs/pr.idx")
    cur = database.cursor()
    iter = cur.first()
    while iter:
        entryPrice = int(iter[0].decode("utf-8"))
        if operator == "<":
            if entryPrice < price:
                # get the aid
                key = iter[1].decode("utf-8").split(',')[0]
                records.append(key.encode('utf-8'))
        elif operator == ">":
            if entryPrice > price:
                # get the aid
                key = iter[1].decode("utf-8").split(',')[0]
                records.append(key.encode('utf-8'))
        elif operator == "<=":
            if entryPrice <= price:
                # get the aid
                key = iter[1].decode("utf-8").split(',')[0]
                records.append(key.encode('utf-8'))
        elif operator == ">=":
            if entryPrice >= price:
                # get the aid
                key = iter[1].decode("utf-8").split(',')[0]
                records.append(key.encode('utf-8'))
        elif operator == "=":
            if entryPrice == price:
                # get the aid
                key = iter[1].decode("utf-8").split(',')[0]
                records.append(key.encode('utf-8'))
        else:
            break
        iter = cur.next()

    cur.close()
    database.close()
    return records

if __name__ == '__main__':
    print(evalDate('<','2018/11/05'))
    print(evalDate('>','2018/11/05'))
    print(evalDate('=','2018/11/05'))
    print(evalDate('<=','2018/11/05'))
    print(evalDate('>=','2018/11/05'))
    print(evalPrice('<','30'))
    print(evalPrice('>','30'))
    print(evalPrice('=','30'))
    print(evalPrice('<=','30'))
    print(evalPrice('>=','30'))
