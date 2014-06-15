#!/usr/bin/python3

import argparse
import random


def main(args):
    fh = open(args.input, "r")
    cols = map(int, args.cols.split(','))
    content = fh.read()

    split = content.find('\n', content.find("@data")) + 1
    header = content[:split]
    #data = content[split:]
    data = [x.split(',') for x in content[split:].split('\n') ]

    for col in cols:
        countToUpdate = round(args.perc / 100 * len(data))
        for item in range(countToUpdate):
            finished = False
            while not finished:
                row = random.randint(0, len(data)-2)
                if data[row][col] != '?':
                    finished = True
                    data[row][col] = '?'
    
    print(header)
    for line in data:
        print(','.join(line))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Unkown introducer')
    parser.add_argument('input', help='weka input file')
    parser.add_argument('cols', help='list of columns to introduce unkown')
    parser.add_argument('perc', type=float, help='percentage of unkown data  introduced on each col')
    args = parser.parse_args()

    exit(main(args))



# vim: set expandtab ts=4 sw=4:
