import collections
from collections import Counter
import math

import operator


def bm25():
    run3 =[]
    with open ("inverted_index.txt","r") as f:
        inv_ind={}

        for line in f:
            lis={}
            word = line.split()
            i=1
            while(i<len(word)):
                lis[word[i]]=int(word[i+1])
                i=i+2
            inv_ind[word[0]]=lis
    tok =0
    with open("doc_length.txt","r") as f1:
        doc_length = {}
        for line in f1:
            doc = line.split()
            doc_length[doc[0]] = doc[1]
            tok = tok + int(doc[1])
    print doc_length["CACM-0001"]
    rel_doc = {}
    rel_doc1 = {}
    #rel_doc[2] = ["CACM-2434","CACM-2863","CACM-3078"]
    query_ind = collections.OrderedDict()
    #query = "i am interested in articles written either by prieve or udo pooch prieve b pooch u".split()
    total = 0
    with open("queries.txt",) as f3:
        for line in f3:
            word = line.split()
            query = word[1:]
            temp = Counter(query)
            q = {}
            for val in temp.iteritems():
                q[val[0]] = val[1]
                total = total + val[1]
            query_ind[word[0]] = q
    with open("cacm.rel","r") as f4:
        for line in f4:
            rel = line.split()
            if rel_doc.has_key(rel[0]):
                rel_doc[rel[0]].append(rel[2])
            else:
                rel_doc[rel[0]] = [rel[2]]
    print rel_doc["2"]
    N = 3204
    avdl = float(tok/len(doc_length))
    print avdl
    bm_score={}
    #print query_ind
    #print inv_ind["prieve"]
    for qid in query_ind.keys():
        print qid
        for doc in doc_length:
            #print doc
            k1 = 1.2
            k2 = 100
            dl = int(doc_length[doc])
            K = float(k1 * ((1-0.75)+ (0.75 * (dl/avdl))))
            bm = 0
            q = query_ind[qid]
            #print q
            for terms in q:
                if inv_ind.has_key(terms):
                    R = 0
                    ri =0
                    fi =0
                    #print terms
                    ni = len(inv_ind[terms])
                    t = inv_ind[terms]
                    if doc in t:
                        fi = t[doc]
                    qfi = q[terms]
                    if rel_doc.has_key(qid):
                        R = len(rel_doc[qid])
                        for docs in rel_doc.get(qid):
                            temp = inv_ind[terms]
                            if docs in temp:
                                ri = ri + 1
                    num1 = float((ri+0.5)/(R-ri+0.5))
                    deno1 = float((ni-ri+0.5)/(N-ni-R+ri+0.5))
                    term1 = num1/deno1
                    dterm = float(((k1 + 1)*fi)/(K +fi))
                    qterm = float(((k2 + 1)*qfi)/(k2+qfi))
                    bm = bm + (math.log(term1,2)*dterm * qterm)
            bm_score[doc] = bm
        sorted_bm = sorted(bm_score.items(), key=operator.itemgetter(1), reverse=True)
        i=1
        #total_rel = len(rel_doc)
        rel_retrieved = 0
        precision = 0
        recall = 0
        doc_type = "N"
        for val in sorted_bm:
            if (i < 101):
                if qid in rel_doc :
                    #print rel_doc[qid]
                    #print  val[0]
                    total_rel = len(rel_doc[qid])
                    if val[0] in rel_doc[qid]:
                        doc_type ="R"
                        rel_retrieved = rel_retrieved + 1
                        print rel_retrieved
                        precision = float(rel_retrieved) / float(i)
                        print precision
                        recall = float(rel_retrieved) / float(total_rel)
                    else:
                        doc_type = "N"
                        print rel_retrieved
                        precision = float(rel_retrieved) / float(i)
                        print precision
                        recall = float(rel_retrieved) / float(total_rel)
                run3.append(str(qid) + " " + "Q0 " + str(val[0]) + " " + str(i) + " " + str(val[1]) + " BM25 "+doc_type+" "
                            +str(precision)+" "+str(recall))
                i = i + 1
            else:
                break
    with open ("run3.txt","w+") as f5:
        for v in run3:
            f5.write(v)
            f5.write("\n")
    f5.close()













bm25()

        

        
