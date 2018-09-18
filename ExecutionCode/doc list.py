i=1
with open ("Doc_list.txt","w") as doc:
    while i<= 3204:
        lnt=len(str(i))
        lnt=4-lnt

        doc.write("CACM-"+("0"*lnt)+str(i)+"\n")
        i+=1
