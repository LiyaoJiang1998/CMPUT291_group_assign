import re
import time
from nonkeySearch import *
from queryEval import *

def intersectResults(queryResults):
    '''
    takes input of a list of list of aids found by each conditionals
    eg.             [[b'1003735318', b'1003735660', b'1002787981'],
                    [b'1003735318', b'1269098382', b'1001612872'],
                    [b'1003735318', b'1370676359', b'1396178670']]
    '''
    if not queryResults:
        return list()
    finalResults = set(queryResults[0])
    for s in queryResults:
        finalResults.intersection_update(s)
    return list(finalResults)

'''
Get a query from user

Inputs: none

Returns:
    key_conditional: a list of tuples for keys, tuple in format (left, operator, right)
    nonkey_conditional: a list of tuples for nonkeys, tuple in format (left, operator, right)
    terms: a list of terms
'''
def getQueryInput():
    confirm = False
    full = True
    while not confirm:
        terms = list()
        exact_terms = list()
        partial_terms = list()
        price_conditional = list()
        date_conditional = list()
        nonkey_conditional = list()
        aids = []
        ids = []
        query = input('Please enter query: ')
        if query == "output=brief":
            full = False
            continue
        elif query == "output=full":
            full = True
            continue

        print('your query was: ')
        print(query)
        c = input('confirm? \'y\' to proceed, \'q\' to quit, anything else to retry: ')
        if c == 'y':
            #get all the conditional statements
            invalid = False
            conditionals = re.findall('[^ ]+[ ]*(?:=|>=|<=|<|>)[ ]*[^ ]+', query)
            for i in range(0,len(conditionals)):
                query = query.replace(conditionals[i], '')
                temp = conditionals[i].replace(' ', '')
                m = re.search('(?:=|>=|<=|>|<)', temp)
                tup = (temp[0:m.start()], temp[m.start():m.end()], temp[m.end():])
                if tup[0] == 'date':
                    date_conditional.append(tup)
                elif tup[0] == 'price':
                    price_conditional.append(tup)
                elif tup[0] == "output" and tup[1] == "=":
                    if tup[2] == "brief":
                        full = False
                    elif tup[2] == "full":
                        full = True
                    else:
                        print("Invalid input, please try again")
                        invalid = True
                        break
                else:
                    if tup[0] != "location" and tup[0] != "cat":
                        print("Invalid input, please try again")
                        invalid = True
                        break
                    nonkey_conditional.append(tup)
            if invalid:
                continue
            #get all the terms
            # terms = re.findall('(?:^| )[^ <>=]+(?:$| )', query)
            terms = re.findall('[a-zA-Z0-9\_\-]+%?', query)
            for term in terms:
                if re.match('^(?!.*%).*$', term):
                    exact_terms.append(term)
                else:
                    partial_terms.append(term.replace('%',''))

            for date in date_conditional:
                # print('date')
                aids.append(evalDate(date[1], date[2]))
            for price in price_conditional:
                # print('price')
                aids.append(evalPrice(price[1], price[2]))
            for exact_term in exact_terms:
                # print('eterm')
                aids.append(exaTermQuery(exact_term))
            for partial_term in partial_terms:
                # print("pterm")
                aids.append(nonExaTermQuery(partial_term))
            if aids:
                ids = intersectResults(aids)
                for nonkey in nonkey_conditional:
                    ids = infoQuery(nonkey, ids)
            else:
                if nonkey_conditional:
                    ids = getAllAids()
                    for nonkey in nonkey_conditional:
                        ids = infoQuery(nonkey, ids)
            if full:
                # print(ids)
                results = getRecords(ids)
                for i in results:
                    print(i)
            else:
                records = getRecords(ids)
                for record in records:
                    m = re.search('<ti>.*<\/ti>', record[1])
                    value = m.group(0).replace('<ti>','').replace('/{ti}>','')
                    print(record[0] + " " + value)

        if c == 'q':
            return

    #time
    #start_time = time.time()



def main():
    getQueryInput()

if __name__ == "__main__":
    # start_time = time.time()
    main()
    # print("--- %s seconds ---" % (time.time() - start_time))
