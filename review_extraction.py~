import urllib2
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient

proxy_support = urllib2.ProxyHandler({'http':"http://ipg_2011016:9461866128@192.168.1.103:3128"})
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)

client = MongoClient('127.0.0.1', 27017)
db = client.reviews
collection = db.motox

url="http://www.flipkart.com/moto-x-16-gb/product-reviews/ITMDTHJKZA6EBURU?pid=MOBDSGU27YGJAZNB"
data = urllib2.urlopen(url).read()
soup = BeautifulSoup(data)
#print soup.find('div',{'class':"review-section helpful-review-container"})
#print "\n\n\n yogendra"
#print soup.find('div',{'class':"review-section helpful-review-container"}).select('strong')[1].text
n=int(soup.find('div',{'class':"review-section helpful-review-container"}).select('strong')[1].text)
#print n

"""if n%10==0:
	loop = n/10
else:
	loop = (n/10)+1"""

for i in [0]:
	param='&start='+str(i*10)
	try:
		data = urllib2.urlopen(url+param).read()
		soup = BeautifulSoup(data)
		y = list(soup.find_all('div',{'class':"fclear fk-review fk-position-relative line "}))
		for each in y:
			summary = each.find('div',{'class':"unit size1of5 section1"})
			star = summary.div.div['title']
			print star

			t = summary.find('div',{'class':"date line fk-font-small"}).text
			time_of_review=re.sub("[\n]*[/ ]+"," ",t)
			print t
			print time_of_review
			title= each.find('div',{'class':"lastUnit size4of5 section2"}).strong.text
			title= re.sub("[\n]*[/ ]+"," ",title)
			review= each.find('div',{'class':"lastUnit size4of5 section2"}).p.text
			review=re.sub("[\n]*[/ ]+"," ",review)
			post={"Rating":star,"Time":time_of_review,"Title":title,"Review":review}
			ids=collection.insert(post)
	except:
		print i

