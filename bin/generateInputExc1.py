#!/usr/bin/python3

import argparse
import numpy
import os

parser = argparse.ArgumentParser(description='Excersice 1 generator')
parser.add_argument('training', help='weka training file')
parser.add_argument('validation', help='weka validation file')
parser.add_argument('output', help='output dir')
args = parser.parse_args()


confidences = numpy.arange(0, 0.501, 0.025)
for confidence in confidences:
    if confidence==0:   confidence=0.001
    filename = "%s/tree_conf_%.3f.out" % (args.output, confidence)
    cmd = ('java -Xmx256m -classpath /usr/share/java/weka.jar ' + 
      'weka.classifiers.trees.J48  -t %s -T %s -C %.4f > %s') \
      % (args.training, args.validation, confidence, filename)
    print(cmd)
    os.system(cmd)

# vim: set expandtab ts=4 sw=4:
