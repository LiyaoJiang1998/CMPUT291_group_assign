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
    key_conditional = list()
    nonkey_conditional = list()

    confirm = False
    while not confirm:
        query = input('Please enter query: ')
        print('your query was: ')
        print(query)
        c = input('confirm? \'y\' to proceed, \'q\' to quit, anything else to retry: ')
        if c == 'y':
            break 
        if c == 'q':
            return key_conditional, nonkey_conditional, terms
    
    #time
    #start_time = time.time()

    #get all the conditional statements
    conditionals = re.findall('[^ ]+[ ]*(?:=|>=|<=|<|>)[ ]*[^ ]+', query)
    for i in range(0,len(conditionals)):
        query = query.replace(conditionals[i], '')
        temp = conditionals[i].replace(' ', '')
        m = re.search('(?:=|>=|<=|>|<)', temp)
        tup = (temp[0:m.start()], temp[m.start():m.end()], temp[m.end():])
        if tup[0] == 'date' or tup[0] == 'price':
            key_conditional.append(tup)
        else:
            nonkey_conditional.append(tup)
    
    #get all the terms
    # terms = re.findall('(?:^| )[^ <>=]+(?:$| )', query)
    terms = re.findall('[a-zA-Z\_\-]+%?', query)
    for i in range(0, len(terms)):
        terms[i] = terms[i].lower()
    
    #end time
    #print("--- %s seconds ---" % (time.time() - start_time))
    return key_conditional, nonkey_conditional, terms
    
def main():
    key_conditional, nonkey_conditional, terms = getQueryInput()
    print(key_conditional)
    print(nonkey_conditional)
    print(terms)

if __name__ == "__main__":
    # start_time = time.time()
    main()
    # print("--- %s seconds ---" % (time.time() - start_time))