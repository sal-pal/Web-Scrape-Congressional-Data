from bs4 import BeautifulSoup
import mechanize
import cookielib
import re
import urllib2
import csv




"""BOT CHEAT SHEET FOR MECHANIZE AND CLASS CREATION FOR ERROR HANDLING"""

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#This error is needed to break the while loop.
def LinkNotFoundError(Exception):
    def __init__(self):
        pass




"""MAPPING NAMES TO INDICES IN ORDER TO PREPARE DATA FOR GRAPH CONSTRUCTOR."""

sen_names = 'C:\Users\Sal\Desktop\PythonPract\Web Scraping\CongrSrape\SenatorsNames113.csv'
f = open(sen_names,'r')
names = f.readlines()

indices = range(105)
indexed_names = []
for i in range(105):
    indexed_names.append((names[i],indices[i]))

indexed_names = dict(indexed_names)




"""COLLECTING COSP NETWORK DATA FROM ALL ELLIGIBLE BILLS"""

url = 'http://thomas.loc.gov/home/LegislativeData.php?&n=Browse&c=113'
br.open(url)
req = br.click_link(text='Senate Amendments')
br.open(req)


illformatted = []
edge_list = []
while True:
    try:
        next_page = br.click_link(text='NEXT PAGE') 

    except LinkNotFoundError:
        break

    else:
        br.open(next_page)
        links = []

    #Collecting links to pages containing cosp info. 
    for l in br.links(text="Cosponsors"):
        links.append('http://thomas.loc.gov' + l.url)

    #Collecting cosp names and retrieving their indices from indexed_names. 
    for url in links:
        f = urllib2.urlopen(url)
        soup = BeautifulSoup(f)
        cosp_tags = soup('a',text=re.compile("Sen"))                  
        cosp_indx = []
        for name in cosp_tags:
            if name.string == 'Senate Executive Report':
                del name
            else:
                cosp_indx.append(indexed_names.get(name.string+'\n'))

        #Creating a edge pairings.
        for i in cosp_indx:
            if cosp_indx.index(i) == cosp_indx.index(cosp_indx[-1]):        
                break
            else:
                for elem in cosp_indx[cosp_indx.index(i)+1:]:               
                    edge_list.append((i,elem))
                    if elem == None:
                        i = cosp_indx.index(elem)
                        tag = cosp_tags[i]
                        illformatted.append(tag.string)
                    with open('C:\Users\Sal\Desktop\PythonPract\Web Scraping\CongrSrape\EdgeList113th.csv','a') as f:
                        write = csv.writer(f)
                        write.writerow((i,elem))
                        
    
                    
            







