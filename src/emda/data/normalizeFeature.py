from sys import argv
from sys import stdout
from os import mkdir
from os import path
from shutil import copy
from shutil import rmtree
import tarfile
from json import load

from numpy import array

from common import getFeatureInfo
from common import normalize

def genFeatureAfterNormalize(fin, fout, desc, mins, maxs):
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
        tmp = None
        for i in range(cntFeatures):
            features[i]['isNormalize'] = tmp if features[i].get('isNormalize') is None else features[i]['isNormalize']   

            feature[i] = eval(feature[i])
            if features[i]['isNormalize']: 
                feature[i] = normalize(feature[i], maxs[i], mins[i])
            l = repr(feature[i]) if i == 0 else l + ',%s' % repr(feature[i])

            tmp = features[i]['isNormalize']

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
    genFeatureAfterNormalize(fin, fout, conf, mins, maxs)
    fin.close()
    fout.close()

    copy('%s/%s.json' % (source, inName), '%s/%s.json' % (output, outName))
    flck = open('%s/normalize.lock' % output, 'w')
    flck.close()

    tar = tarfile.open(outPath, 'w')
    tar.add(output, arcname=outName) 
    tar.close()
    rmtree(source)
    rmtree(output)

if __name__ == '__main__':
    main()
