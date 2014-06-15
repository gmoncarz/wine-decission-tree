#!/usr/bin/python3

import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Unkown filler')
    parser.add_argument('input', help='weka input file')
    parser.add_argument('perc', type=float, help='percentage of unkown data  introduced on each col')
    args = parser.parse_args()


    cmd = r'java -Xmx256m -classpath /usr/share/java/weka.jar weka.filters.unsupervised.attribute.AddNoise -P %.2f < %s' \
      % (args.perc, args.input)

    os.system(cmd)

# vim: set expandtab ts=4 sw=4:
