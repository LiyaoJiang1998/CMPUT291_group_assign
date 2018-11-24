import re
import time

'''
Get a query from user

Inputs: none

Returns:
    conditionals: a list of tuples, tuple in format (left, operator, right)
    terms: a list of terms
'''
def getQueryInput():
    conditionals = list()
    terms = list()

    confirm = False
    while not confirm:
        query = input('Please enter query: ')
        print('your query was: ')
        print(query)
        c = input('confirm? \'y\' to proceed, \'q\' to quit, anything else to retry: ')
        if c == 'y':
            break 
        if c == 'q':
            return conditionals, terms
    
    #time
    #start_time = time.time()

    #get all the conditional statements
    conditionals = re.findall('[^ ]+[ ]*(?:=|>=|<=|<|>)[ ]*[^ ]+', query)
    for i in range(0,len(conditionals)):
        query = query.replace(conditionals[i], '')
        temp = conditionals[i].replace(' ', '')
        m = re.search('(?:=|>=|<=|>|<)', temp)
        conditionals[i] = (temp[0:m.start()], temp[m.start():m.end()], temp[m.end():])
    
    #get all the terms
    # terms = re.findall('(?:^| )[^ <>=]+(?:$| )', query)
    terms = re.findall('[a-zA-Z\_\-]+%?', query)
    for i in range(0, len(terms)):
        terms[i] = terms[i].lower()
    
    #end time
    #print("--- %s seconds ---" % (time.time() - start_time))
    return conditionals, terms
    
def main():
    conditionals, terms = getQueryInput()
    print(conditionals)
    print(terms)

if __name__ == "__main__":
    # start_time = time.time()
    main()
    # print("--- %s seconds ---" % (time.time() - start_time))