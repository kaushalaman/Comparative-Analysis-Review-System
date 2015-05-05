from pymongo import MongoClient
import re

client = MongoClient('127.0.0.1', 27017)
db=client.reviews_copy2
collection=db.motox

for i in collection.find():
        if i['Review']!=[]:
                r=[]
                for j in i['Review']:
                        j=i['Review']
                        j=re.sub("\n+"," ",j)
                        j=re.sub("\s[0-9]\)",". ",j)
                        j=re.sub("\.+",". ",j)
                        j=re.sub(">+"," ",j)
                        j=j.lower()
                        j=re.sub("\s+"," ",j)			
                        r.append(j)
                print r			
                collection.update({"_id": i['_id']}, {"$set": {"Review": j}})
                collection.update({"_id": i['_id']}, {"$set": {"Review": re.sub("\s[0-9]\)",". ",i['Review'])}})
                collection.update({"_id": i['_id']}, {"$set": {"Review": re.sub("\s+"," ",i['Review'])}})
                collection.update({"_id": i['_id']}, {"$set": {"Review": i['Review'].lower()}})
