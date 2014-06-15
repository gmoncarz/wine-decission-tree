#!/usr/bin/python3

import random
import argparse

parser = argparse.ArgumentParser(description='Split training and validation set')
parser.add_argument('trainingPerc',  type=int, 
                   help='an integer for the accumulator')
parser.add_argument('input', help='Input file')
parser.add_argument('--header', action='store_true', help='Tells if input file has header', )
args = parser.parse_args()

input = open(args.input, "r")
training = open(args.input + ".training.out", "w")
validation = open(args.input + ".validation.out", "w")

if args.header:
    header = input.readline()
    training.write(header)
    validation.write(header)

for line in input.readlines():
    rnd = random.random()
    fh = training if rnd*100<=args.trainingPerc else validation
    fh.write(line)

input.close()
training.close()
validation.close()

# vim: set expandtab ts=4 sw=4:
