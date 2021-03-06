import nltk
import pickle
import random
from nltk.corpus import conll2000
from nltk.chunk.util import conlltags2tree
from pymongo import MongoClient
from nltk.corpus import stopwords
from collections import OrderedDict



stop = stopwords.words('english')

test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])


client = MongoClient('127.0.0.1', 27017)
db = client.reviews
collection = db.motox
l = []


class ChunkParser(nltk.ChunkParserI):

        def __init__(self, train_sents):
                train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)] for sent in train_sents]
                self.tagger = nltk.TrigramTagger(train_data)

        def parse(self, sentence):
                pos_tags = [pos for (word,pos) in sentence]
                tagged_pos_tags = self.tagger.tag(pos_tags)
                chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
                conlltags = [(word, pos, chunktag) for ((word,pos),chunktag) in zip(sentence, chunktags)]
                return conlltags2tree(conlltags)


chunker = ChunkParser(train_sents)
print chunker.evaluate(test_sents)
f = open('chunker.pickle', 'w')
pickle.dump(chunker, f)
f.close()

patterns = """
                NP:
                {<NN>+}
                {<NNS>+}
                {<CD>+<NNS|NN|NNP>}
                {<DT|PP\$>?<JJ>*<NN>}
                
        """
chunker = nltk.RegexpParser(patterns)

f = open('chunker.pickle', 'r')
chunker = pickle.load(f)

d={}

def array_form(name):   
        if len(name)!=0:
                for i in name:
                        temp=""
                        for j in range(len(i)):
                                temp=temp+" "+i[j][0]
                        l.append(temp)

def sub_leaves(tree, node):
        p=[t.leaves() for t in tree.subtrees(lambda s: s.node == node)]
        return p

        
def output(tree1):
        array_form(sub_leaves(tree1,'NP'))
        return l
p=[]
for i in collection.find():
        p.append(i['_id'])
        t=collection.find_one({"_id": random.choice(p)})
        #print "///////////////////////////////////"
        #print t['Review'].lower()
        s = nltk.sent_tokenize(i['Review'].lower())
        ss=[nltk.word_tokenize(sent) for sent in s]
        pp=[nltk.pos_tag(sent) for sent in ss]
        for j in pp:
                #print "---------------------------------------"
                #print j
                ttt= chunker.parse(j)
                #print ttt
                too= output(ttt) #ther is some error
                for k in too:
                        if k not in stop:
                                if d.has_key(k):
                                        d[k]=d[k]+1
                                else:
                                        d[k]=1
d = OrderedDict(sorted(d.items(), key=lambda x: x[1]))
d=sorted(d, key=d.get)

print d[-40:]
print len(d)
