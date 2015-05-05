from pymongo import MongoClient
import re

client = MongoClient('127.0.0.1', 27017)
db=client.reviews
collection=db.motox

month ={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sept':'09','Oct':'10','Nov':'11','Dec':'12'}

for i in collection.find():
        print i
        try:
                d=i['Time']
                t=d.split()
                t[0]=t[0]
                t[2]='20'+t[2]
                t[1]=month[t[1]]
                time=" ".join(t)
                collection.update({"_id": i['_id']}, {"$set": {"Time": time}})
        except:
                print "none"
