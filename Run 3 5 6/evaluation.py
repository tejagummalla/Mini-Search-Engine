import collections


def evaluation():
    with open("run3-stem.txt","r") as f1:
        statistics = {}
        statistics1 = {}
        for lines in f1:
            temp = lines.split()
            if statistics1.has_key(temp[0]):
                statistics1[temp[0]].append(temp[1:])
            else:
                statistics1[temp[0]] = [temp[1:]]
            if "R" in temp[6]:
                if statistics.has_key(temp[0]):
                    statistics[temp[0]].append(temp[1:])
                else:
                    statistics[temp[0]] = [temp[1:]]
    average_precision=[]

    patk={}
    #print statistics["42"]
    for values in statistics.iterkeys():
        i = statistics[values]
        #print values
        total_precision = 0
        total_rel = len(i)
        for count in i:
            total_precision = total_precision + float(count[6])
        average_precision.append(float(total_precision) / float(total_rel))

    with open("run3-stem.txt", "r") as f:
        q_list = []
        mrr = 0
        count = 0
        for line in f:
            word = line.split()
            # print word[0]
            if word[0] not in q_list and word[6] == "R":
                mrr += float(word[7])
                count = count + 1
                q_list.append(word[0])

        MRR = mrr / 6

    f2 = open("run3-stem-eval.txt", "w+")
    print len(average_precision)
    MAP = float(sum(average_precision)) / float(len(average_precision))
    print MAP
    print MRR
    f2.write("MAP " + str(MAP) + "\n")
    f2.write("MRR " + str(MRR) + "\n")
    # calculate p@k
    for values in statistics1.iterkeys():
        temp = statistics1[values]
        pat5 = temp[4][6]
        pat20 = temp[19][6]
        patk[values] = [pat5, pat20]
    f2.write("P@K for k = 5 , 20")
    f2.write("\n")
    for values in patk.iteritems():
        f2.write(values[0] + " " + str(values[1][0]) + " " + str(values[1][1]) + "\n")








evaluation()
