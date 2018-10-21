#!/usr/bin/python
import urllib2
import html2text
import hashlib
import pickle
import BeautifulSoup
import re
import sys
import ssl

url=sys.argv[1]
#"http://www.szukajwarchiwach.pl/92/81/0/4/177/str/1/1/15#tabSkany"
baseurl="https://www.szukajwarchiwach.pl"

def download_and_cache(url):
    cachefile="/tmp/" + hashlib.md5(url).hexdigest() + ".cache"
    try:
        data=pickle.load(open(cachefile,"rb"))
        print "read %s from cachefile %s" % (url,cachefile)
    except (IOError,ValueError):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        data=urllib2.urlopen(url,context=ctx).read()
        pickle.dump(data,open(cachefile,"wb"))
        print "save %s to cachefile %s" % (url,cachefile)
    return data

def download_and_save(url,filename):
    data=download_and_cache(url)
    f=open(filename,'w')
    f.write(data)
    f.close()

data=download_and_cache(url)
soup = BeautifulSoup.BeautifulSoup(data)
for link in soup.findAll('a'):
#        print link.get('href')
    text=link.getText()
    if "File: " in link.getText():
        filename=text.split()[1]
        origurl=link.get('href')
        saveurl=origurl.replace('medium','save')
        download_and_save(baseurl+saveurl,filename)
