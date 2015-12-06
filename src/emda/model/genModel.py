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

def getDataset(fin):
    data = []
    target = []

    while True:
        l = fin.readline().strip()
        if len(l) == 0:
            break
        feature = [i.strip() for i in l.split(',')]
        cntFeature = len(feature) - 1
        for i in range(cntFeature):
            feature[i] = eval(feature[i])
        data.append(feature[:-1])
        target.append(feature[-1])
        
    return {'data':array(data), 'target':array(target)}

def getModel(dataset, conf):
    func = 'algorithm.%s(' % conf['algorithm']
    paras = conf['parameters'].keys()
    if len(paras) != 0:
        value = conf['parameters'][paras[0]] if conf['parameters'][paras[0]].isdigit() else '\'%s\'' % conf['parameters'][paras[0]]
        func = func + '%s=%s'  % (paras[0], value)
        for para in paras[1:]:
            value = conf['parameters'][para] if conf['parameters'][para].isdigit() else '\'%s\'' % conf['parameters'][para]
            func = func + ', %s=%s'  % (para, value) 
    func = func + ')'
    #print 'debug[39] func = %s' % func

    mdl = eval(func)

    mdl.fit(dataset['data'], dataset['target'])

    return mdl

def main():
    confPath = path.abspath(argv[1])
    confDir = path.dirname(confPath)
    confName = path.splitext(path.basename(confPath))[0]
    output = '%s/%s' % (confDir, confName)

    tarPath = path.abspath(argv[2])
    tarDir = path.dirname(tarPath)
    tarName = path.splitext(path.basename(tarPath))[0]
    source = '%s/%s' % (tarDir, tarName)

    f = open(confPath, 'r')
    conf = load(f)
    f.close()

    tar = tarfile.open(tarPath, 'r')
    tar.extractall(path=tarDir)
    tar.close()

    fin = open('%s/%s.csv' % (source, tarName), 'r')
    fin.readline()

    try:
        mkdir(output)
    except WindowsError, err:
        print err
        pass
    
    dataset = getDataset(fin)
    print 'debug[81] data = %s' % str(dataset['data'])
    print 'debug[81] target = %s' % str(dataset['target'])
    fin.close()
    mdl = getModel(dataset, conf)
    print 'debug[83] score = %s' % str(mdl.score(dataset['data'], dataset['target']))
    joblib.dump(mdl, '%s/%s.clf' % (output, confName), compress=3)

    copy(confPath, '%s/%s.json' % (output, confName))
    tar = tarfile.open('%s.model' % output, 'w')
    tar.add(output, arcname=confName) 
    tar.close()
    rmtree(source)
    rmtree(output)

if __name__ == '__main__':
    main()
