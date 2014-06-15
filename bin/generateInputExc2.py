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
parser.add_argument('validation', help='weka validation file')
parser.add_argument('output', help='output dir')
args = parser.parse_args()


methods = ['moda', 'modaclase']
rangeGen = numpy.arange(0, 85.5, 2.5)
confidences = numpy.arange(0, 0.501, 0.025)

print('method,fillPerc,confidence,leaves,treeSize,performanceValidation,performanceTraining')
for method in methods:
    # Generate the Dataset
    for perc in rangeGen:
        genDataset = "%s/dataset_faltantes_%.2f_%s.arff" % (args.output, perc, method)
        cmd = './ind_faltantes.py %s %.2f  %s > %s' % \
          (args.training, perc, method, genDataset)
        print('# ' + cmd)
        os.system(cmd)

        # generate the treesa
        for confidence in confidences:
            if confidence==0:   confidence=0.001
            treefile = "%s/tree_faltantes_%.2f_%s_conf_%.3f.out" % (args.output, perc, method, confidence)
            cmd = ('java -Xmx256m -classpath /usr/share/java/weka.jar ' + 
              'weka.classifiers.trees.J48  -t %s -T %s -C %.4f > %s') \
               % (genDataset, args.validation, confidence, treefile)
            print('# ' + cmd)
            os.system(cmd)
            
            procOutput = process(treefile)
            print("%s,%.2f,%s,%s,%s,%s,%s" % (method, perc, 
              procOutput['confidence'],
              procOutput['leaves'],
              procOutput['treeSize'],
              procOutput['performanceValidation'],
              procOutput['performanceTraining']))

# vim: set expandtab ts=4 sw=4:
