'''

Assignment: Take list created at end and

(1) Print out the subject organism

(2) Print out the percentage of hits for that organism

(3) Only print the above for subject organisms that make up more than 1% of the hits

'''

import re
import os

cwd = os.getcwd()
for fn in os.listdir(cwd):
    #print(fn)
    h = re.match('.*nr$', fn)

    #if h:
        #print(h.group())

    if h:
        print(fn)
        f = fn
        fopen = open(f, 'r')
        fread = fopen.readlines()
        hitDic = {}

        for hit in fread:
            cols = hit.strip()
            cols = cols.split('\t')
            
            subject = re.search('\[.*\]', cols[1])
            if subject:
                #print(sseq.group())
                sseq = subject.group()
              
            if sseq not in hitDic:
                hitDic[sseq] = 1
            else:
                hitDic[sseq] = hitDic[sseq] + 1

        #for contig in hitDic.items():
         #   print(contig)

 
        hitList = sorted(hitDic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
        #print(type(sortDic))
        #print(fn)
        
