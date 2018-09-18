import operator
import math
import collections

def length(tf_idf,d,inv,d_len):

    length=0
    for item in tf_idf:
        if d in inv[item]:
            length = length + math.pow(inv[item][d]*tf_idf[item]/d_len,2)

    return length


def query_length(tf_idf,q):

    length=0
    inv=invert_query(q)
    for item in inv:
        length+=math.pow(inv[item],2)
        

    return length
def denominator(q,d,tf_idf,inv,d_len):
    q_inv=invert_query(q)
    num=0
    num_q=1
    num_d=1
    #print d
    for item in q_inv:
        num_q+=math.pow(q_inv[item],2)
        if d in inv[item]:
            num_d+=math.pow(inv[item][d]*tf_idf[item]/d_len,2)
            #print "num :",num
    num= num_q*num_d
    return num

def invert_query(q) :
    inv={}
    for item in q:
        if item in inv:
            inv[item]=inv[item]+1
        else:
            inv[item]=1
    return inv

def numerator(q,d,tf_idf,inv,d_len):

    q_inv=invert_query(q)
    num=0
    #print d
    for item in q_inv:
        if d in inv[item]:
            num_q=q_inv[item]
            num_d=inv[item][d]*tf_idf[item]/d_len
            num+= num_q*num_d
            #print "num :",num
    return num

def cosine(q,d,tf_idf,inv,d_len):
    cos_similarity=numerator(q,d,tf_idf,inv,d_len)/(math.sqrt(query_length(tf_idf,q)*length(tf_idf,d,inv,d_len)))
    return cos_similarity

    

def get_term_frequency ():

    
    
    inverted_index = {}
    term_frequency={}
    t_frequency={}
    do_array={}
    doc_len={}
    #f_array=readurls()
    table_inverted=[]
    # retriving the stored invereted list
    #quer=invert_query(query)
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
    with open ("doc_length.txt","r") as f:
        doc_len={}
        for line in f:
            word=line.split()
            doc_len[word[0]]=word[1]
    with open ("queries.txt","r") as q:
        que={}
        for line in q:
            word=line.split()
            que[word[0]]=word[1:]
            #break

    rel_doc={}
    with open("cacm.rel","r") as f4:
        for line in f4:
            rel = line.split()
            if rel_doc.has_key(rel[0]):
                rel_doc[rel[0]].append(rel[2])
            else:
                rel_doc[rel[0]] = [rel[2]]
        #print rel_doc["2"]
    idf={}
    ND=len(doc_len)
    print ND
    with open("idf.txt","w") as i:
        for term in inv_ind:
                idf[term]=math.log(ND*1.0/len(inv_ind[term]))
                #tf_idf[term]=id
                i.write(term+" "+str(idf[term])+"\n")
    #with open("tf_idf_task1.txt","w") as tf:
    with open("PR-Run1-tfidf.txt","w") as tf:
        #que = collections.OrderedDict()
        #print que
        for var in sorted(que):
            print var
            do_array={}
            target_inv={}
            tf_q=invert_query(que[var])
            #-retriving all inverted index with respect to the query
            print que[var]
            #print doc_len
            for item in que[var]:

                if item in inv_ind:
                    for doc in doc_len:
                        if doc in inv_ind[item] and doc not in do_array :
                            do_array[doc]=1
                    #if item not in target_inv:            
                    target_inv[item]=inv_ind[item]
                            #Creating the score list based on the query
            score={}
            #print target_inv
            for item in do_array:
                temp=0
                dclt=doc_len[item]
                for element in target_inv:
                    #print "1"
                    #print element
                    #print item
                    if item in target_inv[element]:
                        #print "1"
                        #print idf[element]
                        temp+=idf[element]*target_inv[element][item]/int(dclt)*1.0*tf_q[element]/len(que[var])
                        #print target_inv[element][item]
                score[item]=temp
                #print temp

            doc_sort=sorted(score.items(), key=operator.itemgetter(1), reverse=True)
            i=1
            '''
            for item in doc_sort:
                #tf.write(str(item[0]))
                tf.write(var+'   Q0'+' '*8)
                t=str(item[0])
                tf.write(t)
                tf.write(" "*(20- len(str(item[0]))))
                tf.write(str(i)+ "  "*(5-len(str(i))))
                i+=1
                tf.write(str(item[1])+" "*(15- len(str(item[0]))))
                tf.write("tf_idf")
                tf.write("   "+str(round(p,3))+"  "+str(round(rec,3)))
                tf.write("\n")
                if(i==101):
                    break
            '''
            if var in rel_doc :
                p=0
                r=0
                ret=0
                for item in doc_sort:
                    if item[0] in rel_doc[var]:
                        ret+=1
                        r=r+1
                        id_doc="R"
                    else:
                        ret+=1
                        id_doc="NR"
                    p=r*1.0/ret*1.0
                    rec=r*1.0/len(rel_doc[var])
                    #pre.write(var+"   "+str(ret)+"     "+str(p)+"  "+str(rec)+"  "+id_doc+"\n")
                    tf.write(var+'   Q0'+' '*8)
                    t=str(item[0])
                    tf.write(t)
                    tf.write(" "*(20- len(str(item[0]))))
                    tf.write(str(i)+ "  "*(5-len(str(i))))
                    i+=1
                    tf.write(str(item[1])+" "*(15- len(str(item[0]))))
                    tf.write("tf_idf")
                    tf.write("  "+id_doc+"   "+str(round(p,3))+"  "+str(round(rec,3)))
                    tf.write("\n")
                    if(ret==100):
                        break

                    
            '''   
            else:
                ret=1
                for item in doc_sort:
                    pre.write(var+'   '+str(ret)+' '*4)
                    t=str(item[0])
                    pre.write(t)
                    pre.write(" "*(15- len(str(item[0]))))
                    pre.write(str(item[1])+" "*4)
                    pre.write("NR   "+str(round(0,3))+"  "+str(round(0,3)))
                    pre.write("\n")
                    if(ret==20):
                        break
                    ret=ret+1
            '''
get_term_frequency()

