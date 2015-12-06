from sys import argv
from sys import stdout
from os import mkdir
from os import path
from decimal import Decimal
from shutil import copy
from shutil import rmtree
import tarfile
from json import load

from numpy import array

from common import getFeatureInfo

def genFeatureAfterFill(fin, fout, desc, mins, maxs, cnts, sums):
    head = desc['features'][0]['name']
    for f in desc['features'][1:]:
        head =  head + ',%s' % f['name']
    head = head + ',class'
    fout.write('%s\n' % head)

    features = desc['features']
    cntFeatures = len(features)

    while True:
        l = fin.readline().strip()
        if len(l) == 0:
            break
        feature = [i.strip() for i in l.split(',')]
        l = ''
        for i in range(cntFeatures):
            feature[i] = eval(feature[i])
            #print 'debug[32]', feature[i], maxs
            #raw_input()
            if feature[i] == 'min':
                feature[i] = mins[i]
            elif feature[i] == 'max':
                feature[i] = maxs[i]
            elif feature[i] == 'mean':
                feature[i] = sums[i] / cnts[i] if cnts[i] > 0 else 0
            else:
                feature[i] = feature[i]
            l = repr(feature[i]) if i == 0 else l + ',%s' % repr(feature[i])

        l = l + ',%s' % feature[-1]
        fout.write('%s\n' % l)

def main():
    inPath = path.abspath(argv[1])
    inDir = path.dirname(inPath)
    inName = path.splitext(path.basename(inPath))[0]
    source = '%s/%s' % (inDir, inName)

    tar = tarfile.open(inPath, 'r')
    tar.extractall(path=inDir)
    tar.close()

    if path.exists('%s/normalize.lock' % source):
        print 'error[44] already normalized!'
        rmtree(source)
        return -1

    if path.exists('%s/dummy.lock' % source):
        print 'error[65] already dummy!'
        rmtree(source)
        return -1

    outPath = path.abspath(argv[2])
    outDir = path.dirname(outPath)
    outName = path.splitext(path.basename(outPath))[0]
    output = '%s/%s' % (outDir, outName)

    try:
        mkdir(output)
    except WindowsError, err:
        print err

    f = open('%s/%s.json' % (source, inName), 'r')
    conf = load(f)
    f.close()

    fin = open('%s/%s.csv' % (source, inName), 'r')
    fin.readline()

    (mins, maxs, cnts, sums) = getFeatureInfo(fin, conf)

    fin.seek(0)
    fin.readline()

    fout = open('%s/%s.csv' % (output, outName), 'w')
    genFeatureAfterFill(fin, fout, conf, mins, maxs, cnts, sums)
    fin.close()
    fout.close()

    copy('%s/%s.json' % (source, inName), '%s/%s.json' % (output, outName))

    tar = tarfile.open(outPath, 'w')
    tar.add(output, arcname=outName) 
    tar.close()
    rmtree(source)
    rmtree(output)

if __name__ == '__main__':
    main()
