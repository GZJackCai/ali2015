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
from sklearn.externals import joblib

import algorithm

def genPredict(conf, fout):
    if not conf['isEnsembled']:
        tarPath = path.abspath(conf['main']['model'])
        tarDir = path.dirname(tarPath)
        tarName = path.splitext(path.basename(tarPath))[0]
        source = '%s/%s' % (tarDir, tarName)

        tar = tarfile.open(tarPath, 'r')
        tar.extractall(path=tarDir)
        tar.close()

        clf = joblib.load('%s/%s.clf' % (source, tarName))

        tarPath = path.abspath(conf['main']['sample'])
        tarDir = path.dirname(tarPath)
        tarName = path.splitext(path.basename(tarPath))[0]
        source = '%s/%s' % (tarDir, tarName)

        tar = tarfile.open(tarPath, 'r')
        tar.extractall(path=tarDir)
        tar.close()

        f1 = open('%s/%s.csv' % (source, tarName), 'r')
        f1.readline()

        tarPath = path.abspath(conf['main']['feature'])
        tarDir = path.dirname(tarPath)
        tarName = path.splitext(path.basename(tarPath))[0]
        source = '%s/%s' % (tarDir, tarName)

        tar = tarfile.open(tarPath, 'r')
        tar.extractall(path=tarDir)
        tar.close()

        f2 = open('%s/%s.csv' % (source, tarName), 'r')
        f2.readline()

        j = 0
        while True:
            l = f2.readline().strip()
            if len(l) == 0:
                break
            feature = [i.strip() for i in l.split(',')]
            cntFeature = len(feature) - 1
            for i in range(cntFeature):
                feature[i] = eval(feature[i])
            
            (ID, user_id, item_category, item_id, CLASS) = [i.strip() for i in f1.readline().strip().split(',')]
            fout.write('%d,%d,%s\n' % (eval(user_id), eval(item_id), clf.predict(array(feature[:-1]))[0]))
            stdout.write('debug[64] j = %d\r' % j)
            j = j + 1

        f1.close()
        f2.close()

        tarPath = path.abspath(conf['main']['model'])
        tarDir = path.dirname(tarPath)
        tarName = path.splitext(path.basename(tarPath))[0]
        source = '%s/%s' % (tarDir, tarName)
        rmtree(source)

        tarPath = path.abspath(conf['main']['sample'])
        tarDir = path.dirname(tarPath)
        tarName = path.splitext(path.basename(tarPath))[0]
        source = '%s/%s' % (tarDir, tarName)
        rmtree(source)

        tarPath = path.abspath(conf['main']['feature'])
        tarDir = path.dirname(tarPath)
        tarName = path.splitext(path.basename(tarPath))[0]
        source = '%s/%s' % (tarDir, tarName)
        rmtree(source)
        
    else:
        pass

def main():
    confPath = path.abspath(argv[1])
    confDir = path.dirname(confPath)
    confName = path.splitext(path.basename(confPath))[0]
    output = '%s/%s' % (confDir, confName)

    f = open(confPath, 'r')
    conf = load(f)
    f.close()

    try:
        mkdir(output)
    except WindowsError, err:
        print err
        pass
    
    fout = open('%s/%s.csv' % (output, confName), 'w')
    fout.write('user_id,item_id,class\n')
    genPredict(conf, fout)
    fout.close()

    copy(confPath, '%s/%s.json' % (output, confName))
    tar = tarfile.open('%s.predict' % output, 'w')
    tar.add(output, arcname=confName) 
    tar.close()
    rmtree(output)

if __name__ == '__main__':
    main()
