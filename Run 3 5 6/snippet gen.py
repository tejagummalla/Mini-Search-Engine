import collections
import re

import operator


def snippetgen():
    with open("common_words.txt", "r") as f:
        common_words = []
        for lines in f:
            common_words.append(lines.rstrip("\n"))
    with open("queries.txt", ) as f3:
        query_ind =collections.OrderedDict()
        for line in f3:
            word = line.split()
            query = word[1:]
            q=[]
            for term in query:
                if term not in common_words:
                    q.append(term)
            query_ind[word[0]] = q
    print query_ind["1"]

    with open("run3.txt","r") as f1:
        statistics1 = collections.OrderedDict()
        for lines in f1:
            temp = lines.split()
            if statistics1.has_key(temp[0]):
                statistics1[temp[0]].append(temp[2])
            else:
                statistics1[temp[0]] = [temp[2]]
    print  statistics1["1"]
    rel_doc = collections.OrderedDict()
    for val in statistics1.iterkeys():
        i = 0
        for values in statistics1[val]:
            if (i < 15):
                if rel_doc.has_key(val):
                    rel_doc[val].append(values)
                else:
                    rel_doc[val] = [values]
            else:
                break
            i = i + 1
    #print rel_doc["1"]
    sentences = collections.OrderedDict()
    for qid in rel_doc.iterkeys():
        for doc in rel_doc[qid]:
            with open("C:\Project ir\cacm\\"+doc+".html", "r+") as f:
                # print f
                line = f.read()
                # line=line.lower
                line = re.sub(r'<[^>]*>', "",line)
                line = re.sub(r'\n'," ",line)
                line = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', line)

                #line = re.split(r'\n',line)
            sentences[doc] = line
    #print sentences["CACM-1523"]
    selected_sent={}
    sel_sent_queries = collections.OrderedDict()
    for qid in rel_doc.iterkeys():
        print qid
        for doc in rel_doc[qid]:
            sent_score =[]
            for sent in sentences[doc]:
                sent = str(sent).lower()
                temp = sent.split()
                score = 0
                for words in temp:
                    #print query_ind["1"]
                    if words in query_ind[qid]:
                        score= score+1
               # print sent + "\n"
                #print score
                sent_score.append([sent,score])
            sorted_score = sorted(sent_score, key=operator.itemgetter(1), reverse=True)
            if len(sorted_score) >= 2:
                #print "hello"
                selected_sent[doc] = [sorted_score[0][0],sorted_score[1][0]]
            else:
                selected_sent[doc] = [sorted_score[0][0]]
        sel_sent_queries[qid] = selected_sent

    print query_ind["1"]
    print selected_sent["CACM-1657"]
    fo = open("snippet.txt","w+")
    for qid in sel_sent_queries.iterkeys():
        fo.write("Query: "+str(qid)+"\n")
        for docs in sel_sent_queries[qid]:
            fo.write("Document: "+str(docs)+"\n")
            for sent in selected_sent[docs]:
                temp = sent.split()
                w =""
                for v in temp:
                    if v in query_ind[qid]:
                        w = w + " ***" +v+"*** "
                    else:
                        w = w +" "+ v
                #print len(selected_sent[docs])
                if len(str(sent)) < 101:
                    fo.write(w+" \n")
                    str1 = "-" * 105
                    fo.write(str1+"\n")
                else:
                    str1 = "-" * 105
                    fo.write(w[0:100] + "...\n")
                    fo.write(str1 + "\n")
        str1 = "-" * 105
        fo.write(str1 + "\n")





snippetgen()