import collections
import math

import operator


def kld():
    with open ("inverted_index.txt","r") as f:
        inv_ind={}
        document ={}

        for line in f:
            lis={}
            word = line.split()
            i=1
            while(i<len(word)):
                lis[word[i]]=int(word[i+1])
                if document.has_key(word[i]):
                    document[word[i]].append(word[0])
                else:
                    document[word[i]]= [word[0]]
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
    #rel_doc[2] = ["CACM-2434","CACM-2863","CACM-3078"]

    #query = "i am interested in articles written either by prieve or udo pooch prieve b pooch u".split()
    total = 0
    with open("queries.txt",) as f3:
        query_ind = collections.OrderedDict()
        for line in f3:
            word = line.split()
            query = word[1:]
            temp = collections.Counter(query)
            q = {}
            for val in temp.iteritems():
                q[val[0]] = val[1]
                total = total + val[1]
            query_ind[word[0]] = q

    with open("run3.txt", "r") as f1:
        rel_doc1 = collections.OrderedDict()
        for lines in f1:
            temp = lines.split()
            if rel_doc1.has_key(temp[0]):
                rel_doc1[temp[0]].append(temp[2])
            else:
                rel_doc1[temp[0]] = [temp[2]]
    print query_ind
    rel_doc = collections.OrderedDict()
    for val in rel_doc1.iterkeys():
        i=0
        for values in rel_doc1[val]:
            if(i<15):
                if rel_doc.has_key(val):
                    rel_doc[val].append(values)
                else:
                    rel_doc[val]= [values]
            else:
                break
            i= i+1


    with open("common_words.txt","r") as f:
        stop_words =[]
        for lines in f:
            stop_words.append(lines.rstrip("\n"))


    #calculate the kld score
    #print statistics1["64"]
    #print rel_doc["64"]
    s_t = collections.OrderedDict()
    for qid in query_ind:
        print qid
        pr_t = 0
        pc_t =0
        term_score ={}
        new_rel= rel_doc[qid]
        for d in new_rel:
            rel_terms = document[d]
        for term in rel_terms:
            query_terms = []
            for val in query_ind[qid]:
                query_terms.append(val)
            if term not in stop_words:
                tf1 = 0
                d1 =0
                tf_cor = 0
                tf2_cor = 0
                d1_cor = 0
                for docs in new_rel:

                    temp = inv_ind[term]
                    if docs in temp:
                        tf1 = tf1 + temp[docs]
                    else:
                        tf1 = tf1 + 0
                    tf2=0
                    for origin_term in query_ind[qid]:
                        #print origin_term
                        if origin_term in inv_ind:
                            t = inv_ind[origin_term]
                            if docs in t:
                                tf2 = tf2 + t[docs]
                            else:
                                tf2 = tf2 + 0
                    d1 = d1 + tf2
                pr_t = float(tf1)/float(d1)
                #print pr_t
                for docs_cor in document:
                    temp = inv_ind[term]
                    if docs_cor in temp:
                        tf_cor = tf_cor + temp[docs_cor]
                    else:
                        tf_cor = tf_cor + 0
                    for origin_term in query_ind[qid]:
                        #print origin_term
                        if origin_term in inv_ind:
                            t = inv_ind[origin_term]
                            if docs_cor in t:
                                tf2_cor = tf2_cor + t[docs_cor]
                            else:
                                tf2_cor = tf2 + 0
                    d1_cor = d1_cor + tf2_cor
                pc_t = float(tf_cor)/float(d1_cor)
            #print pc_t
                term_score[term] = float(pr_t * math.log(pr_t/pc_t))
        s_t[qid] = term_score

    for qid in s_t:
        print qid
        sorted_kl = sorted(s_t[qid].items(), key=operator.itemgetter(1), reverse=True)
        print sorted_kl
    fo = open("queries_expanded_pseudo_run3.txt","w+")
    for q in s_t.iterkeys():
        fo.write(str(q) + " ")
        i = 1
        for val in s_t[q]:
            if i<11:
                print str(val) + "\n"
                fo.write(str(val)+" ")
            i+= 1
        fo.write("\n")



kld()