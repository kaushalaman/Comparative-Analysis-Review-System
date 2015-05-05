import nltk
from pymongo import MongoClient
from nltk.corpus import stopwords
from collections import OrderedDict
import random
import fileinput
import sys

#client = MongoClient('127.0.0.1', 27017)
#db1=client.reviewofmotox
#collection=db1.motox
happy=0.0
unhappy=0.0
features={'camera':[[],[],[]],'picture':[[],[],[]],'display':[[],[],[]],'processor':[[],[],[]],'battery':[[],[],[]],'control':[[],[],[]],'touch':[[],[],[]],'memory':[[],[],[]],'nfc':[[],[],[]],'design':[[],[],[]],'price':[[],[],[]],'experience':[[],[],[]]}

f=open('negative-words.txt','r')
neg = f.read().split('\n')[:-1]
f.close()
f=open('positive-words.txt','r')
pos=f.read().split('\n')[:-1]

ow=[]
but=0
def but_rule(feat,ow,sent):
        split_sent=sent.split('but')
        but_clause=nltk.word_tokenize(split_sent[1])
        orient=0
        if feat in but_clause:
                for opinion in ow:
                        if opinion in but_clause:
                                orient=orient+word_orient(opinion,feat,split_sent[1])
                if orient!=0:
                        return orient
                else:
                        for opinion in ow:
                                if opinion in nltk.word_tokenize(split_sent[0]):
                                        orient=orient+word_orient(opinion,feat,split_sent[0])
                        if orient!=0:
                                return -1*orient
                        else:
                                return 0
                        

def check_neg(opinion):
        if opinion=='no' or opinion=='not' or opinion=='never':
                return True
        else:
                return False            

def dist(opinion,feat,sent):
        op=sent.index(opinion)
        try:
                fe=sent.index(feat)
                d=fe-op
                if d>0:
                        return d
                elif d<0:
                        return -1*d
                else:
                        return 0.000001
        except:
                return 9999999
                

def neg_rule(op,feat,sent):
        tokens=nltk.word_tokenize(sent)
        try:
                now=tokens[tokens.index(op)+1]
                orient=word_orient(now,feat,sent)
                try :
                        ow.pop(ow.index(now))
                        if orient==0 or orient==1:
                                return -1
                        else:
                                return -1*orient
                
                except:
                
                        if orient==0 or orient==1:
                                return -1
                        else:
                                return -1*orient
        except:
                return -1
        
        

def word_orient(opinion,feat,sent):
        orient=0
        tokens=nltk.word_tokenize(sent)
        if check_neg(opinion):
                orient=neg_rule(opinion,feat,sent)
        else:
                if opinion in neg:
                        orient=-1.0
                elif opinion in pos:
                        orient=1.0
                else:
                        orient=0.0
        d=dist(opinion,feat,tokens)
        final_op=(orient/d)
        return final_op
                
#f=open('motox.txt')
#product = "Moto X"
product = sys.stdin.readline().strip();
#dproduct={}
#dproduct["name"]=product

#for line in open('motox.txt','r').readlines():
for line in sys.stdin:
        line.strip()
        for j in line.split('/////////////'):
                tokens=nltk.word_tokenize(j)
                #print "_________________________"
                #print tokens
                #print "_________________________"
                t=nltk.pos_tag(tokens)
                temp={}
                feat_o={}
                ow=[]
                but=0
                for k in t:
                        if features.has_key(k[0]):
                                temp[k[0]]=0
                                feat_o[k[0]]=''
                        if k[0]=='but':
                                but=1
                        if k[1]=='JJ' or k[1]=='JJR' or k[1]=='JJS' or k[1]=='NN' or k[1]=='NNS' or k[1]=='RB' or k[1]=='RBR' or k[1]=='VB' or k[1]=='VBG':
                                ow.append(k[0])
                #print str(temp) + "but:" + str(but)
                for feat in temp:
                        if but==1:
                                temp[feat]=but_rule(feat,ow,j)
                        else:
                                for opinion in ow:
                                        temp[feat]=temp[feat]+word_orient(opinion,feat,j)
                        if temp[feat]>0:
                                feat_o[feat]=1
                        elif  temp[feat]<0:
                                feat_o[feat]=-1
                        else:
                                feat_o[feat]=0
                #print feat_o
                for c in feat_o:
                        if feat_o[c]==1:
                                features[c][0].append(product)
                        elif feat_o[c]==-1:
                                features[c][1].append(product)
                        else:
                                features[c][2].append(product)
i=0
for each in features:
        try:
                print product+"`"+each+"`"+str(len(features[each][0]))+"`"+str(len(features[each][1]))+"`"+str(len(features[each][2]))
                happy=happy+float(len(features[each][0]))
                unhappy=unhappy+float(len(features[each][1]))
        except:
                pass
#print features
rating=happy/unhappy
print product+"`"+str(rating)
#keys=features.keys()
#r=random.choice(keys)
#db2=client.reviewofmotox
#collection1=db2.motox
#print "----A Random Sample Negative Review about "+r+" ----"
#review=collection1.find({'_id':random.choice(features[r][1])})
#for i in review:
#       print i['Review']
                
