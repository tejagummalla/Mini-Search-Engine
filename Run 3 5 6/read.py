import collections
from collections import Counter

query_ind = collections.OrderedDict()
with open("queries.txt", ) as f3:
    query_ind = collections.OrderedDict()
    for line in f3:
        word = line.split()

        query = word[1:]
        query_ind[word[0]] = query
with open("queries_expanded_pseudo_run3.txt","r") as f2:
    for line in f2:
        w = line.split()
        q = w[1:]
        for item in q:
            query_ind[w[0]].append(item)


f1 = open("expanded-queries-pseudo_run3.txt","w+")
for values in query_ind.iterkeys():
    f1.write(str(values) + " ")
    for v in query_ind[values]:
        f1.write(str(v)+" ")
    f1.write("\n")
f1.close()

