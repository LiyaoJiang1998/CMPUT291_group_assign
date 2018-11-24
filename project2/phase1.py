import re

#out put file locations
terms = './outputs/terms.txt'
pdates = './outputs/pdates.txt'
prices = './outputs/prices.txt'
ads = './outputs/ads.txt'


def processPdate(date, aid, cat, loc):
    global pdates
    f = open(pdates, 'a')
    f.write(date + ':' + aid + ',' + cat + ',' + loc + '\n')
    f.close()

'''
A function used to take a input string and aid and write to terms.txt

inputs:
    info: a string
    aid: the id of the ad
'''
def processTerms(info, aid):
    global terms
    #remove special chars
    specialCharList = re.findall('\&\#[0-9]+;', info)
    for c in specialCharList:
        info = info.replace(c, '')
    info = info.replace('&apos;', '\'')
    info = info.replace('&quot;', '\"')
    info = info.replace('&amp;', '&')
    
    termList = re.findall('[0-9a-z\_\-]{3,}',info)
    f = open(terms, 'a')
    for t in termList:
        f.write(t+':'+aid+'\n')
    f.close()

'''
A function used to take information from the xml line and output to 4 files
'''
def process(line):
    m = re.search('<aid>[0-9]+<\/aid>', line)
    #get aid
    aid = m.group(0).replace('<aid>','').replace('</aid>','')
    m = re.search('<ti>.+<\/ti>', line)

    #get title
    title = m.group(0).replace('<ti>','').replace('/ti>','').lower()

    #get desc
    m = re.search('<desc>.+</desc>', line)
    desc = m.group(0).replace('<desc>','').replace('/desc>','').lower()

    #output to terms.txt
    processTerms(title, aid)
    processTerms(desc,aid)

    
    #get date
    m = re.search('<date>.*</date>', line)
    date = m.group(0).replace('<date>','').replace('</date>','').lower()

    #get category
    m = re.search('<cat>.*</cat>', line)
    category = m.group(0).replace('<cat>','').replace('</cat>','').lower()

    #get location
    m = re.search('<loc>.*</loc>', line)
    location = m.group(0).replace('<loc>','').replace('</loc>','')

    #output to pdate.txt
    processPdate(date, aid, category, location)
    
    
'''
A function used to clear existing output txt files
'''
def clearOutputs():
    global terms, pdates, prices, ads
    temp = open(terms, 'w')
    temp.close()
    temp = open(pdates, 'w')
    temp.close()
    temp = open(prices, 'w')
    temp.close()
    temp = open(ads, 'w')
    temp.close()

def main():
    info = open("./1k.txt", "r")
    line = info.readline()

    clearOutputs()

    while line is not '':
        #print(line)
        if re.match('<ad>.+<\/ad>', line):
            process(line)
        
        line = info.readline()

if __name__ == "__main__":
    main()