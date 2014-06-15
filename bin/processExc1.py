#!/usr/bin/python3

import argparse
import re;


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
    match = re.findall(r'Correctly Classified Instances.*?(\d+\.\d+)\s*\%\s*$', content,  re.MULTILINE)
    ret['performanceTraining'] = match[0]
    ret['performanceValidation'] = match[1]
    
    return ret


#    conf_re = re.compile(r'-C (\d+\.\d+)')
#    corr_re = re.compile(r'Correctly Classified Instances.*(\d+\.\d+)\s*\%')
#    for line in fh:
#        if conf_re.search(line):
#            print(line)
#        elif corr_re.search(line):
#            print(line)


def main(files):
    info = []
    for filename in files:
        info.append(process(filename))

    print('confidence,leaves,treeSize,performanceValidation,performanceTraining')
    for atom in sorted(info, key=(lambda x: x['confidence'])):
        print("%s,%s,%s,%s,%s" % (atom['confidence'], atom['leaves'], atom['treeSize'],
          atom['performanceValidation'], atom['performanceTraining']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Excersice 1 generator')
    parser.add_argument('files', nargs="+",  help='weka training file')
    args = parser.parse_args()

    exit(main(args.files))
# vim: set expandtab ts=4 sw=4:
