#!/usr/bin/python3

import argparse
import numpy
import os
import re



def process(filename):
    fh = open(filename, 'r')
    content = fh.read()
    fh.close()

    ret = {}
    match = re.search(r'-C (\d+\.\d+)', content)
    ret['confidence'] = match.group(1)
    match = re.search(r'Size of the tree\s*\:[^\d]*(\d+)', content)
    ret['treeSize'] = match.group(1)
    match = re.search(r'Number of Leaves\s*\:[^\d]*(\d+)', content)
    ret['leaves'] = match.group(1)
    match = re.findall(r'Correctly Classified Instances.*?(\d*\.?\d+)\s*\%\s*$', content,  re.MULTILINE)
    ret['performanceTraining'] = match[0]
    ret['performanceValidation'] = match[1]
    
    return ret




parser = argparse.ArgumentParser(description='Excersice 2 dataset generator')
parser.add_argument('training', help='weka training file')
parser.add_argument('output', help='output dir')
args = parser.parse_args()


methods = ['supervisado', 'ancho', 'frecuencia']
confidences = numpy.arange(0, 0.501, 0.025)
#confidences = numpy.arange(0, 0.501, 0.25)

print('method,bin,confidence,leaves,treeSize,performanceValidation,performanceTraining')

# Run the iterations with 
for method in methods:
    if method == 'supervisado':
        bins = [1]
    else:
        bins = numpy.arange(1, 20.5, 1)
    # Generate the Dataset for equal-with adn equal-freq
    for bin in bins:
        genDataset = "%s/dataset_disc_%d_%s.arff" % (args.output, bin, method)
        cmd = './discret.py %s %d  %s > %s' % \
          (args.training, bin, method, genDataset)
        print('# ' + cmd)
        os.system(cmd)

        # generate the treesa
        for confidence in confidences:
            if confidence==0:   confidence=0.001
            treefile = "%s/tree_discret_%d_%s_conf_%.3f.out" % (args.output, bin, method, confidence)
            cmd = ('java -Xmx256m -classpath /usr/share/java/weka.jar ' + 
              'weka.classifiers.trees.J48  -t %s -split-percentage %d -C %.4f > %s') \
               % (genDataset, 80, confidence, treefile)
            print('# ' + cmd)
            os.system(cmd)
            
            procOutput = process(treefile)
            print("%s,%.2f,%s,%s,%s,%s,%s" % (method, bin, 
              procOutput['confidence'],
              procOutput['leaves'],
              procOutput['treeSize'],
              procOutput['performanceValidation'],
              procOutput['performanceTraining']))

# vim: set expandtab ts=4 sw=4:
