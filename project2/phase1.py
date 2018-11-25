import re
import time
import sys

#out put file locations
terms = './outputs/terms.txt'
pdates = './outputs/pdates.txt'
prices = './outputs/prices.txt'
ads = './outputs/ads.txt'
# data = './10.txt'
data = sys.argv[1]

'''
a function used to write ads to ads.txt in the desired format
'''
def processAds(aid, line, adf):
    adf.write(aid + ':' + line)

'''
a function used to write prices to prices.txt in the desired format
'''
def processPrice(price, aid, cat, loc, prf):
    prf.write('{:>12}'.format(price) + ':' + aid + ',' + cat + ',' + loc + '\n')

'''
A function used to write pdates to pdates.txt in the desired format

inputs:
    date: date of ad
    aid: id of ad
    cat: categorty of ad
    loc: location of ad
    pdf: file to append info to
'''
def processPdate(date, aid, cat, loc, pdf):
    pdf.write(date + ':' + aid + ',' + cat + ',' + loc + '\n')


'''
A function used write to terms.txt

inputs:
    info: a string
    aid: the id of the ad
    tf: file to append terms to
'''
def processTerms(info, aid, tf):
    #remove special chars
    specialCharList = re.findall('\&\#[0-9]+;', info)
    for c in specialCharList:
        info = info.replace(c, '')
    info = info.replace('&apos;', '\'')
    info = info.replace('&quot;', '\"')
    info = info.replace('&amp;', '&')

    termList = re.findall('[0-9a-z\_\-]{3,}',info)
    for t in termList:
        tf.write(t+':'+aid+'\n')

'''
A function used to take information from the xml line and output to 4 files

inputs:
    line: a line read from the data file
    tf: file to append terms to
    pdf: file to append pdates to
    prf: file to append prices to
    adf: file to append ads to
'''
def process(line, tf, pdf, prf, adf):
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
    processTerms(title, aid, tf)
    processTerms(desc,aid, tf)

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
    processPdate(date, aid, category, location, pdf)

    #get price
    m = re.search('<price>.*</price>', line)
    price = m.group(0).replace('<price>', '').replace('</price>','')

    #output to prices.txt
    processPrice(price, aid, category, location, prf)

    #output to ads.txt
    processAds(aid, line, adf)


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
    global data, terms, pdates, prices, ads
    info = open(data, "r")
    line = info.readline()

    clearOutputs()
    tf = open(terms, 'a')
    pdf = open(pdates, 'a')
    prf = open(prices, 'a')
    adf = open(ads, 'a')
    while line is not '':
        #print(line)
        if re.match('<ad>.+<\/ad>', line):
            process(line, tf, pdf, prf, adf)
        line = info.readline()
    tf.close()
    pdf.close()
    prf.close()
    adf.close()
    info.close()

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
