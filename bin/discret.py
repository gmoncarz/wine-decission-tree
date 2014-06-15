#!/usr/bin/python3

import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Discretize tool')
    parser.add_argument('input', help='weka input file')
    parser.add_argument('bins', type=int, help='# bins to discretize')
    parser.add_argument('method', choices=('frecuencia', 'ancho', 'supervisado'), 
      help='# bins to discretize')
    args = parser.parse_args()

    if args.method == 'ancho':
      cmd = r'java -Xmx256m -classpath /usr/share/java/weka.jar weka.filters.unsupervised.attribute.Discretize -B %d -R 10,12 < %s' \
        % (args.bins, args.input)
    elif args.method == 'frecuencia':
      cmd = r'java -Xmx256m -classpath /usr/share/java/weka.jar weka.filters.unsupervised.attribute.Discretize -B %d -F -R 10,12 < %s' \
        % (args.bins, args.input)
    else:
      cmd = r'java -Xmx256m -classpath /usr/share/java/weka.jar weka.filters.supervised.attribute.Discretize -c last -R 10,12 < %s' \
        % (args.input)
        
    os.system(cmd)

# vim: set expandtab ts=4 sw=4:
