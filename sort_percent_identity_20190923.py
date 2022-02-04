'''
 Tsv files. break apart by percent idenity

(1) Create master lists for each sub list.

(2) Get the average percent identity for each .tsv file.

(3) Find out why "elmt" still has its '\n'.

(4) Create a dictionary for each master list where the subject organism is the key and the number of times it appears in the master list is the value. 

 
'''

def makeMaster(subList, masList):
    for elmnt in subList:
        elmnt = elmnt.strip()
        masList.append(elmnt)

def makeDict(masList, Dict) :
    for stuff in masList:
        subject = re.search('\[.*\]', stuff)
        if subject:
            sseq =subject.group()
        if sseq not in Dict:
            Dict[sseq]=1
        else:
            Dict[sseq] = Dict[sseq] +1

def printList(sorted_list) :
    for l in sorted_list :
        print(l[0] +'\t' + str(l[1]))


import os
import re
path = os.getcwd()
folder = os.fsencode(path)
filenames = []

for file in os.listdir(folder):
    filename = os.fsdecode(file)
    blastp = re.search('\.tsv$', filename)
    if blastp:
        filenames.append(filename)
masfir30 = []
masmid=[]
masfinal=[]

for f in filenames :
    fopen = open(f, 'r')
    fread= fopen.readlines()

    list1 = []
    subfir30 = []
    submid= []
    subfinal= []
    ident= []

  #  print(f)
    for var in fread:
        cols = var.strip()
        cols = cols.split('\t')
        #print(cols[2])


        #for hit in cols :
        ident.append(float(cols[2]))
    #print(len(fread))
   # print(len(ident))

    #print(str(round(lsum, 2)) + '\t' + str(total) + '\t' + str(round(per, 2)))

        if float(cols[2]) < 30 :
            subfir30.append(var)
        #print(fir30)
        elif float(cols[2]) >= 30 and float(cols[2]) <= 60 :
            submid.append(var)
        elif float(cols[2]) > 60 and float(cols[2]) <=100 :
            subfinal.append(var)
        else :
            print('ERROR!')

    makeMaster(subfir30, masfir30)
    makeMaster(submid, masmid)
    makeMaster(subfinal, masfinal)

   

#for thing in masfir30 :
 #   print(thing)

firDict= {}
midDict= {}
finDict = {}

makeDict(masfir30, firDict)
makeDict(masmid, midDict)
makeDict(masfinal, finDict)

sorted_fir = sorted(firDict.items(), key=lambda kv: kv[1], reverse=True)
sorted_mid = sorted(midDict.items(), key=lambda kv: kv[1], reverse=True)
sorted_fin = sorted(finDict.items(), key=lambda kv: kv[1], reverse=True)

printList(sorted_fin)
    

