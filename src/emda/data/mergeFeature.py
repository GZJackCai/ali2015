from sys import argv
from sys import stdout
from os import mkdir
from os import path
from datetime import datetime
from shutil import copy
from shutil import rmtree
import tarfile
from json import load

from numpy import array

from common import FormatString

def merge(conf, fout, leftFile, rightFile, leftDesc, rightDesc):
    names = []
    for f in conf['features']:
        names.append(f['name'])
        
    head = names[0]
    for name in names[1:]:
        head =  head + ',%s' % name
    head = head + ',class'
    fout.write('%s\n' % head)

    features = conf['features']
    cntFeatures = len(features)

    j = 0
    while True:
        leftLine = leftFile.readline().strip()
        if len(leftLine) == 0:
            break
        leftFeature = [i.strip() for i in leftLine.split(',')]

        rightLine = rightFile.readline().strip()
        if len(rightLine) == 0:
            break
        rightFeature = [i.strip() for i in rightLine.split(',')]


        if leftFeature[-1] != rightFeature[-1]:
            raise Exception("right class %s, left class %s" % (leftFeature[-1], rightFeature[-1]))

        l = ''
        tmp = {'output':None, 'default':None}
        for i in range(cntFeatures):
            features[i]['output'] = tmp['output'] if features[i].get('output') is None else features[i]['output']   
            features[i]['default'] = tmp['default'] if features[i].get('default') is None else features[i]['default']   
            output = FormatString(leftFeature, '<', features[i]['output'])
            output = FormatString(rightFeature, '>', output)
            try:
                value = eval(output)
            except Exception, err:
                if type(err) == ValueError or type(err) == TypeError:
                    value = features[i]['default']
                else:
                    raise err
            l = repr(value) if i ==0 else l + ',%s' % repr(value)

            tmp['output'] = features[i]['output']
            tmp['default'] = features[i]['default']

        l = l + ',%s' % leftFeature[-1]
        fout.write('%s\n' % l)
        j = j + 1
        stdout.write('debug[58] j = %d\r' % j)

def main():
    confPath = path.abspath(argv[1])
    confDir = path.dirname(confPath)
    confName = path.splitext(path.basename(confPath))[0]
    output = '%s/%s' % (confDir, confName)

    leftPath = path.abspath(argv[2])
    leftDir = path.dirname(leftPath)
    leftName = path.splitext(path.basename(leftPath))[0]
    leftSrc = '%s/%s' % (leftDir, leftName)

    tar = tarfile.open(leftPath, 'r')
    tar.extractall(path=leftDir)
    tar.close()

    if path.exists('%s/dummy.lock' % leftSrc):
        print 'error[65] left:[%s] already dummy!' % leftPath
        rmtree(leftSrc)
        return -1
    if path.exists('%s/normalize.lock' % leftSrc):
        print 'error[65] left:[%s] already normalized!' % leftPath
        rmtree(leftSrc)
        return -1

    rightPath = path.abspath(argv[3])
    rightDir = path.dirname(rightPath)
    rightName = path.splitext(path.basename(rightPath))[0]
    rightSrc = '%s/%s' % (rightDir, rightName)

    tar = tarfile.open(rightPath, 'r')
    tar.extractall(path=rightDir)
    tar.close()

    if path.exists('%s/dummy.lock' % rightSrc):
        print 'error[65] right:[%s] already dummy!' % rightPath
        rmtree(rightSrc)
        return -1
    if path.exists('%s/dummy.lock' % rightSrc):
        print 'error[65] right:[%s] already normalized!' % rightPath
        rmtree(rightSrc)
        return -1

    try:
        mkdir(output)
    except WindowsError, err:
        print err

    f = open(confPath, 'r')
    conf = load(f)
    f.close()

    fout = open('%s/%s.csv' % (output, confName), 'w')

    f = open('%s/%s.json' % (leftSrc, leftName), 'r')
    leftDesc = load(f)
    f.close()

    leftFile = open('%s/%s.csv' % (leftSrc, leftName), 'r')
    leftFile.readline()

    f = open('%s/%s.json' % (rightSrc, rightName), 'r')
    rightDesc = load(f)
    f.close()

    rightFile = open('%s/%s.csv' % (rightSrc, rightName), 'r')
    rightFile.readline()
    
    merge(conf, fout, leftFile, rightFile, leftDesc, rightDesc)
    leftFile.close()
    rightFile.close()
    fout.close()

    copy(confPath, '%s/%s.json' % (output, confName))

    tar = tarfile.open('%s.feature' % output, 'w')
    tar.add(output, arcname=confName) 
    tar.close()
    rmtree(leftSrc)
    rmtree(rightSrc)
    rmtree(output)

if __name__ == '__main__':
    main()
