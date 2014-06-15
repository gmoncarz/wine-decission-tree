#!/usr/bin/python3

import argparse
import random
import collections

def moda(lst):
    freq = collections.Counter(lst)
    return freq.most_common()[0][0]

    
def getMode(data):
    ret = {}
    for col in range(len(data[1])):
        colValues = filter((lambda x: x!='?'), map((lambda x: x[col]), data))
        mode = moda(colValues)

        ret[col] = mode
    return ret



def getModeClass(data, classCol):
    ret = {}
    
    classes = list(map((lambda x: x[classCol]), data))
    classCounter = collections.Counter(classes)
    for classItem in classCounter:
        ret[classItem] = {}
        for col in range(len(data[1])):
            if col != classCol:
                #colValues = filter((lambda x: x!='?'), map((lambda x: x[col]), data))
                items = map((lambda x: x[col]), filter((lambda x: x[classCol]==classItem), data))
                items = filter( (lambda x: x!='?'), items)
                mode = moda(items)
                ret[classItem][col] = mode
                
    return ret



def main(args):
    fh = open(args.input, "r")
    content = fh.read()

    # Split the header from data
    split = content.find('\n', content.find("@data")) + 1
    header = content[:split]
    #data = content[split:]
    data = [x.split(',') for x in content[split:].strip().split('\n') ]
    
    classCol = len(data[0])-1
    if args.strategy=='moda':
        mode = getMode(data)
    else:
        mode = getModeClass(data, classCol)

    # Store in unkownCoords, a touple for each row,col of data
    # that has an unkown value.
    unknownCoords = []
    for rowIndex in range(len(data)):
        for colIndex in range(len(data[rowIndex])):
            if data[rowIndex][colIndex] == '?':
                unknownCoords.append((rowIndex,colIndex))

    
    # Shuffle the unkownCoords
    random.shuffle(unknownCoords)
    
    countFill = round(len(unknownCoords) / 100 * args.perc)
    for coord in unknownCoords[:countFill]:
        row = coord[0]
        col = coord[1]
        if args.strategy == 'moda':
            data[row][col] = mode[col]
        else:
            classValue = data[row][classCol]
            data[row][col] = mode[classValue][col]


    print(header)
    for line in data:
        print(','.join(line))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Unkown filler')
    parser.add_argument('input', help='weka input file')
    parser.add_argument('perc', type=float, help='percentage of unkown data  introduced on each col')
    parser.add_argument('strategy', help='unknown fill strategy', choices=('moda', 'modaclase'))
    args = parser.parse_args()

    exit(main(args))



# vim: set expandtab ts=4 sw=4:
