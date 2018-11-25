import re
import time

'''
Get a query from user

Inputs: none

Returns:
    key_conditional: a list of tuples for keys, tuple in format (left, operator, right)
    nonkey_conditional: a list of tuples for nonkeys, tuple in format (left, operator, right)
    terms: a list of terms
'''
def getQueryInput():
    #conditionals = list()
    terms = list()
    exact_terms = list()
    partial_terms = list()
    price_conditional = list()
    date_conditional = list()
    nonkey_conditional = list()

    confirm = False
    full = True
    while not confirm:
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
                else:
                    if tup[0] != "location" or tup[0] != "cat":
                        print("Invalid input, please try again")
                        continue
                    nonkey_conditional.append(tup)

            #get all the terms
            # terms = re.findall('(?:^| )[^ <>=]+(?:$| )', query)
            terms = re.findall('[a-zA-Z\_\-]+%?', query)
            for term in terms:
                if re.match('^(?!.*%).*$', term):
                    exact_terms.append(term)
                else:
                    partial_terms.append(term)
        aids = []
        for date in date_conditional:
            aids.append(evalDate(date[1], date[2]))
        for price in price_conditional:
            aids.append(evalPrice(price[1], price[2]))
        for exact_term in exact_terms:
            aids.append(exaTermQuery(exact_term))
        for partial_term in partial_terms:
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
            print(getRecords(ids))
        else:
            records = getRecords(ids)
            for record in records:
                m = re.search('<ti>.+<\/ti>', records)
                value = m.group(0).replace('<ti>'.,'').replace('/{ti}>','')
                print(record[0] + value)



        if c == 'q':
            return

    #time
    #start_time = time.time()



def main():
    price_conditional, date_conditional, nonkey_conditional, exact_terms, partial_terms = getQueryInput()
    print(price_conditional)
    print(date_conditional)
    print(nonkey_conditional)
    print(exact_terms)
    print(partial_terms)

if __name__ == "__main__":
    # start_time = time.time()
    main()
    # print("--- %s seconds ---" % (time.time() - start_time))
