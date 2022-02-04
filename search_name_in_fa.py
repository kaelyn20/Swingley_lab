import re
import os

path = os.getcwd()
folder = os.fsencode(path)

filenames = []

for file in os.listdir(folder):
    filename = os.fsdecode(file)
    #print(filename)
   
    if re.search('\.fa$', filename):
        filenames.append(filename)
        
elements = ['phage', 'mobile', 'repeat', 'integrase']# 'Phage', 'Mobile', 'Repeat']
 
for f in filenames:
    fin = f
    #print(fin)
    ofin= open(fin, 'r')
    rfin = ofin.readlines()


    print(f)
    for line in rfin:
        line = line.strip()

        if any(elem in line.lower() for elem in elements):
            print(line)

    print()
        
