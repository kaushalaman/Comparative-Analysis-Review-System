import urllib2
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient

#proxy_support = urllib2.ProxyHandler({"http":"http://ipg_2011093:9907865940r@192.168.1.103:3128"})
#opener = urllib2.build_opener(proxy_support)
#urllib2.install_opener(opener)

client = MongoClient('127.0.0.1', 27017)
db = client.reviewofmi3
collection = db.mi3
print "rrrrrrrrrrrrr"
url="http://www.flipkart.com/mi3/product-reviews/ITMDXSVRRERJHZTF?pid=MOBDXSVH7HHHNK8J&rating=1,2,3,4,5&reviewers=all&type=all&sort=most_helpful"
data = urllib2.urlopen(url).read()
soup = BeautifulSoup(data)
print soup
#print soup.find('div',{'class':"review-section helpful-review-container"})
#print "\n\n\n yogendra"
print soup.find('div',{'class':"review-section helpful-review-container"}).select('strong')[1].text
count=int(soup.find('div',{'class':"review-section helpful-review-container"}).select('strong')[1].text)
print count
print "Rishabh Upadhyay"

#n=int(soup.find('span',{'class':"nav_bar_result_count"}).text.split()[0])

"""if n%10==0:
	loop = n/10
else:
	loop = (n/10)+1"""

for i in [0,1,2,3,4,5,6,7,8,9]:
	param='&start='+str(i*10)
	try:
		data = urllib2.urlopen(url+param).read()
		#print data
		soup = BeautifulSoup(data)
		y = list(soup.find_all('div',{'class':"fclear fk-review fk-position-relative line "}))
		for each in y:
			summary = each.find('div',{'class':"unit size1of5 section1"})
			#print summary
			star = summary.div.div['title']
			print star
			t = summary.find('div',{'class':"date line fk-font-small"}).text
			print t
			time_of_review=re.sub("[\n]*[/ ]+"," ",t)
			print t
			title= each.find('div',{'class':"lastUnit size4of5 section2"}).strong.text
			print title
			title= re.sub("[\n]*[/ ]+"," ",title)
			print title
			review= each.find('div',{'class':"lastUnit size4of5 section2"}).p.text
			review=re.sub("[\n]*[/ ]+"," ",review)
			post={"Rating":star,"Time":time_of_review,"Title":title,"Review":review}
			ids=collection.insert(post)
	except:
		print i

