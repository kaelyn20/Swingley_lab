'''READ ME:
Find .tsv files in folder

Go through outfmt 6 blast file from nr blast

Count number of hits per sseq organism

Need to get perc for each nr organism
    Print org
    Print perc

'''

import re
import os

cwd = os.getcwd()
for fn in os.listdir(cwd):
    #print(fn)
    h = re.match('.*tsv$', fn)		#finds files with an ending of .tsv

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

        for contig in hitDic.items():
            print(contig)

 
        hitList = sorted(hitDic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
        #print(type(sortDic))
        #print(fn)
        
