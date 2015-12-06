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
from common import dummy

def genFeatureAfterDummy(fin, fout, desc, mins, maxs):
    names = []
    tmp = {'isDummy':None, 'cntBox':None, 'isFromMax':None}
    for f in desc['features']:
        f['isDummy'] = tmp['isDummy'] if f.get('isDummy') is None else f['isDummy']
        f['cntBox'] = tmp['cntBox'] if f.get('cntBox') is None else f['cntBox']
        f['isFromMax'] = tmp['isFromMax'] if f.get('isFromMax') is None else f['isFromMax']

        if f['isDummy']:
            for i in range(f['cntBox']):
                names.append('%s[%d]' % (f['name'], i))
        else:
            names.append(f['name'])

        tmp['isDummy'] = f['isDummy']
        tmp['cntBox'] = f['cntBox']
        tmp['isFromMax'] = f['isFromMax']

    head = names[0]
    for name in names[1:]:
        head =  head + ',%s' % name
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
        tmp = {'isDummy':None, 'cntBox':None, 'isFromMax':None}
        for i in range(cntFeatures):
            features[i]['isDummy'] = tmp['isDummy'] if features[i].get('isDummy') is None else f['isDummy']
            features[i]['cntBox'] = tmp['cntBox'] if features[i].get('cntBox') is None else f['cntBox']
            features[i]['isFromMax'] = tmp['isFromMax'] if features[i].get('isFromMax') is None else f['isFromMax']

            feature[i] = eval(feature[i])
            if features[i]['isDummy']: 
                feature[i] = dummy(feature[i], maxs[i], mins[i], features[i]['cntBox'], features[i]['isFromMax'])
                cntFeature = len(feature[i])
                for j in range(cntFeature):
                    l = repr(feature[i][j]) if i == 0 and j ==0  else l + ',%s' % repr(feature[i][j])
            else:
                l = repr(feature[i]) if i == 0 else l + ',%s' % repr(feature[i])

            tmp['isDummy'] = features[i]['isDummy']
            tmp['cntBox'] = features[i]['cntBox']
            tmp['isFromMax'] = features[i]['isFromMax']

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
    genFeatureAfterDummy(fin, fout, conf, mins, maxs)
    fin.close()
    fout.close()

    copy('%s/%s.json' % (source, inName), '%s/%s.json' % (output, outName))
    flck = open('%s/dummy.lock' % output, 'w')
    flck.close()

    tar = tarfile.open(outPath, 'w')
    tar.add(output, arcname=outName) 
    tar.close()
    rmtree(source)
    rmtree(output)

if __name__ == '__main__':
    main()
