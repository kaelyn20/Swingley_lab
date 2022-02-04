'''READ ME:
Find .tsv files in folder

Go through outfmt 6 blast file from nr blast

Count number of hits per sseq organism

Need to add code that gets percent - done

Uses functions to open, make dic and get avg.

Finds high hits then re-processes files to count high hits

'''

import re
import os

def processFile(file):
    of = open(file, 'r')
    rf = of.readlines()
    return of, rf 

def processFileLines(fileLines):
    seqDic = {}
    for hit in fileLines:
        cols = hit.strip()
        cols = cols.split('\t')
            
        subject = re.search('\[.*\]', cols[1])
        if subject:
            sseq = subject.group()
              
        if sseq not in seqDic:
            seqDic[sseq] = 1
        else:
            seqDic[sseq] = seqDic[sseq] + 1
    return seqDic

def getAvg(count, total):
    average = (count / total) * 100
    return average


highHits ={}
hhl = []
flist = []


cwd = os.getcwd()
for fn in os.listdir(cwd): 
    
    if re.match('.*tsv$', fn):
        fopen, fread = processFile(fn)
        
        flist.append(fn)
        
        hitDic = processFileLines(fread)

        hitList = sorted(hitDic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)

        print(fn)
        for hit in hitList:
            c = hit[1]
            t = len(fread)
            x = getAvg(c, t)
            #print(hit[0] + '\t' + str(c) + '\t' + str(t) + '\t' + str(x))

            if x > 0.99:
                print(hit[0] + '\t' + str(round(x, 2)))

                cd = re.match('.[cC]andidate\s*[dD]ivision\s*\w*', hit[0])
                hH = re.match('.\w*\s*\w*', hit[0])
                if cd:
                    cd = cd.group()
                    cd = cd[1:]
                    if cd not in hhl:
                        hhl.append(cd)
                    
                elif hH:
                    hH = hH.group()
                    hH = hH[1:]

                    if hH not in hhl:
                        hhl.append(hH)
                else:
                    continue
                
        fopen.close()
        print()

print()

for fn in flist:

    fopen, fread = processFile(fn)
      
    fstr = str(fread)

    print(fn)
    for hit in hhl:
        c = fstr.count(hit)
        t = len(fread)
        x = getAvg(c, t)

        print(hit + '\t' + str(c) + '\t' + str(t) + '\t' + (str(round(x, 2))))

    fopen.close()
    print()
