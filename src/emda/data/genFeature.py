from sys import argv
from sys import stdout
from os import mkdir
from os import path
from time import time
from shutil import copy
from shutil import rmtree
import tarfile
from json import load

from MySQLdb import connect

from common import FormatString
from settings import database


def genFeature(db, fin, fout, conf):
    names = []
    tmp = None
    for f in conf['features']:
        isIgnore = tmp if f.get('isIgnore') is None else f['isIgnore']
        if not isIgnore:
            names.append(f['name'])
        tmp = isIgnore

    head = names[0]
    for name in names[1:]:
        head =  head + ',%s' % name
    head = head + ',class'
    fout.write('%s\n' % head)

    csSel = db.cursor()

    tmp = {'name':None, 'type':None, 'output':None, 'condition':None, 'default':None, 'isIgnore':None, 'isNormalize':None, 'isDummy':None, 'cntBox':None, 'isFromMax':None}

    i = 0
    while True:
        values = []
        reals = []
        sample = fin.readline()
        if len(sample) == 0:
            break
        sample = sample.strip().split(',')

        #max_f = 0
        #sum_f = 0 
        #max_feature = None
        #begin_w = time()
        for feature in conf['features']:
            for j in tmp.keys():
                feature[j] = tmp[j] if feature.get(j) is None else feature[j]

            selSel = conf['outputs'][feature['output']] + conf['types'][feature['type']] + conf['conditions'][feature['condition']]
            selSel = FormatString(sample, '#', selSel)
            selSel = FormatString(values, '$', selSel)
            #print 'debug[69] selSel = %s' % selSel

            #begin_f = time()
            csSel.execute(selSel)
            try:
                values.append(csSel.fetchone()[0])
                if values[-1] is None:
                    values[-1] = feature['default']
            except TypeError, err:
                values.append(feature['default'])
            if not feature['isIgnore']:
                reals.append(values[-1])
            #end_f = time()
            #if (end_f - begin_f) > max_f:
            #    max_f = end_f - begin_f
            #    max_feature = feature['name']
            #sum_f = sum_f + (end_f - begin_f)
            #print 'debug[64] feature = %s, value = %s, cost = %f' % (feature['name'], str(values[-1]), end_f - begin_f)

            for j in tmp.keys(): 
                tmp[j] = feature[j]
        #end_w = time()
        #print 'debug[64] whole cost = %f, sum = %f, max = (%f, %s)' %  (end_w - begin_w, sum_f, max_f, max_feature)

        content = repr(reals[0])
        for real in reals[1:]:
            content =  content + ',%s' % repr(real)
        content = content + ',%s' % sample[4].strip()
        #begin_r = time()
        fout.write('%s\n' % content)
        #end_r = time()
        #print 'debug[90] write cost = %f' %  (end_r - begin_r)
        #raw_input()

        stdout.write('debug[101] i = %d\r' % i)
        i = i + 1

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

    db = connect(database['host'], database['user'], database['password'], database['database'])

    fin = open('%s/%s.csv' % (source, tarName), 'r')
    fin.readline()

    try:
        mkdir(output)
    except WindowsError, err:
        print err

    fout = open('%s/%s.csv' % (output, confName), 'w')
    genFeature(db, fin, fout, conf)
    fin.close()
    rmtree(source)
    fout.close()
    db.close()

    copy(confPath, '%s/%s.json' % (output, confName))
    tar = tarfile.open('%s.feature' % output, 'w')
    tar.add(output, arcname=confName) 
    tar.close()
    rmtree(output)

if __name__ == '__main__':
    main()
