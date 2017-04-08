from collections import Counter, defaultdict, OrderedDict
from itertools import chain, combinations,permutations
import re
import io
import os
import itertools as it
import pandas as pd

wordCounter = {}
freq_item = {}
d4 = {}

class Rules:
    RuleList = []
    def __init__(self, rule, orignalset,support, confidence):
        self.rule = rule
        self.orignalset = orignalset
        self.support = support
        self.confidence = confidence
        self.RuleList.append(self)

def freqitem(support,min_support):
    for word, occurance in wordCounter.items():
        if float(occurance)/float(support) >= min_support:
            freq_item[word] = float(occurance)/float(support)
    return freq_item

def test(filename):
    count = 0
    with open(filename, 'r') as fh:
        for ln in fh:
            d3 = ln.rstrip().lower()
            if count>0:
                d4[re.sub('[\s+]', '', d3)] = count
            count += 1

def Fsupport(filename):
    count = 0
    with open(filename, 'r') as fh:
        for ln in fh:
            d3 = ln.rstrip().lower()
            if count > 0:
                test1=re.sub('[\s+]', ',', d3)
                test2 = test1.split(',')
                test3 = [part.strip() for part in test2 if part != '']
                test4 = ','.join(test3)
                d4[test4]=count
            count += 1
    return count

def getSupportForfreqCombinations(lst):
    fsubsetitem={}
    for l in lst: #list of combinations
        count = 0
        OrignalOccurance = 0
        splittedlines = str(l).split(',')
        for a in list(d4):  # orignal dataset
            splitorignaldata = str(a).split(',')

            for spd in splitorignaldata:
                for cdd in splittedlines:  # split combinations
                    cdd1 = cdd.replace("('", '').replace("'", '').replace(')', '').strip()
                    if cdd1 == spd:
                        count+=1
                if len(l)==count:
                    OrignalOccurance+=1
                    count=0
        if OrignalOccurance>0:
            fsubsetitem[l]=OrignalOccurance
    return fsubsetitem


def preparedata(filename):
    # wordCounter = {}
    with open(filename, 'r') as fh:
        for line in fh:
            # Replacing punctuation characters. Making the string to lower.
            # The split will spit the line into a list.
            word_list = line.replace(',', '').replace('\'', '').replace('.', '').lower().split()
            for word in word_list:
                # Adding  the word into the wordCounter dictionary.
                if word not in wordCounter:
                    wordCounter[word] = 1
                else:
                    # if the word is already in the dictionary updat`e its count.
                    wordCounter[word] = wordCounter[word] + 1
    return wordCounter

def GenerateCombinations(dictionary,K):
    outList = []
    for i in list(dictionary):
        outList+=i
    unique_list = [e for i, e in enumerate(outList) if outList.index(e) == i]
    return unique_list

def GenerateSubsets(lst):
    outList = []
    for i in lst:
        outList+=i
    unique_list = [e for i, e in enumerate(outList) if outList.index(e) == i]
    return unique_list

# main function which is called first when the program is executed
def main():
    # ask user for input the filename, minimum support, and minimum confidence
    filename = raw_input("Enter a file name: ")
    min_support =  raw_input("Enter Minimum support: ")
    min_confidence = raw_input("Enter minimun confidence: ")
    if float(min_support) >1:
        min_support = raw_input("Enter Minimum support between (0 - 1): ")
    if float(min_confidence)>1:
        min_confidence = raw_input("Enter minimun confidence between (0 - 1): ")
    path ='/users/grad/bhalla/assign3/Output.txt'
    min_support = float(min_support)
    min_confidence = float(min_confidence)
    filename = filename.strip()
    # Prepare the data
    preparedata(filename)

    # get teh set of data
    Final_Supprt = Fsupport(filename)-1

    # Frequent itemset
    freqitem(Final_Supprt,min_support)

    # Get the frequent itemset
    print 'First Frequent Set Completed.....!'
    print 'Generating K Frequent Set.....!'

    dikt = {}
    counter = 0
    combntns=[]
    k = 2
    i = 0
    while 1:
        if k ==2:
            a = list(combinations(freq_item.keys(), k))
            b = list(OrderedDict.fromkeys(a))  # pruning and removing duplicate values    
        else:
            combntns = GenerateCombinations(dikt2, k)
            a = list(combinations(combntns, k))
            b = list(OrderedDict.fromkeys(a))  # pruning and removing duplicate values

        dikt2 = {}
        for c in b:  # freqitemset
            OrignalOccurance = 0
            for cd in d4:
                occurance = 0
                splitorignaldata= str(cd).split(',')

                for spd in splitorignaldata:

                    splittedlines = str(c).split(',')

                    for cdd in splittedlines:  # orignal data
                        cdd1 = cdd.replace("('", '').replace("'", '').replace(')', '').strip()
                        if cdd1 == spd:  # run this loop based on the value of K
                            occurance += 1
                    if k == occurance:
                        OrignalOccurance += 1
                        occurance = 0
            if  float(OrignalOccurance)/float(Final_Supprt) >= min_support:
                dikt2[c] = float(OrignalOccurance)/float(Final_Supprt)
        if len(dikt2)==0:
            break
        dikt[k] = dikt2
        k+=1
    print 'K Frequent Set Completed.....!'
    print 'Generating Association Rules.....!'
    #Association Rules generation
    lastSet = []
    subsets = []
    check=0
    finalresult = {}
    for key, val in dikt.items():
        for ks,vs in val.items():
            #make possible combinations
            check=0
            comb=[]
            for val in range(0,len(ks)):
                check+=1
                if check<len(ks):
                    comb += list(combinations(ks, check))
            resultset={}
            resultset = getSupportForfreqCombinations(comb)
            for k,v in resultset.items():
                supportOfV = float(v) / float(Final_Supprt)
                if supportOfV > 0:
                    if vs / (supportOfV) >= min_confidence:
                        Rule = Rules(list(set(k)),list(set(ks)-set(k)), supportOfV, vs / supportOfV)
    print 'Association Rules Completed.....! \n'

    print('file is saved in the following path: /users/grad/bhalla/assign3/Output.txt' + '\n')
    cnt=1

    # Delete file test2.txt
    if os.path.exists(path):
        os.remove(path)
    cnt = 1
    f = open(path, 'w+')
    f.write('Summary: \n')
    f.write('Total rows in the orignal set:' + str(Final_Supprt)+ '\n')
    f.write('Total rules discovered: ' + str(len(Rules.RuleList))+ '\n')
    f.write('Selected measures: support =' + str(min_support) + '  confidence = ' + str(min_confidence)+ '\n')
    f.write('...........................................................................'+ '\n')
    for i in Rules.RuleList:
        f.write('Rule No. {:2},  {:15}==>{:21} [Support: {:4}, Confidence: {:3}] \n'.format(cnt, i.rule,i.orignalset,i.support ,i.confidence))
        cnt += 1
    f.close()
# this will call the main() function first
if __name__ == '__main__':
    main()
