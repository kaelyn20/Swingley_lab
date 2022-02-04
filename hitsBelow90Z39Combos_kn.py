''''

Assignment: What does each section of code do?

'''
import os
import re

path = os.getcwd()

folder = os.fsencode(path)
filenames = []
for file in os.listdir(folder):
    filename = os.fsdecode(file)
    #print(filename)
    tsv = re.search('\.tsv$', filename)
    #print(blastp)
    if tsv:
        filenames.append(filename)

#for l in filenames:
#    print(l)


print('FileName\tHits\tHits<90%\t%Hits<90%')
for f in filenames:
    fin = f
    #print(fin)
    ofin= open(fin, 'r')
    rfin = ofin.readlines()
    cutoff = 90
    #print('The file is ' + fin + '. The cutoff is ' + str(cutoff))

 
    lowList = []
    subList = []


    for hit in rfin:
        cols = hit.strip()
        cols = cols.split()
        #print(cols)
        
        if float(cols[2])< 90:
            subList.append(cols[0])
            subList.append(cols[1])
            subList.append(cols[2])
            lowList.append(subList)

        subList = []

    

    lHits = len(lowList)
    tHits = len(rfin)
    plHit = (lHits / tHits) * 100
    
    print(f + '\t' + str(tHits) + '\t' + str(lHits) + '\t' + str(round(plHit, 2)))

    ofin.close()
    
    
    
    
    
        
    

    
