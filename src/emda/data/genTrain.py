from sys import argv
from sys import stdout
from os import mkdir
from os import path
from random import randrange
from shutil import copy
from shutil import rmtree
import tarfile
from json import load

from MySQLdb import connect

from settings import database
from sql import selDataId
from sql import selData

def genTrain(db, sqls, f, cls, conf):
    csSel = db.cursor()
    csSubSel = db.cursor()

    sqlSel = sqls['selDataId'] % cls

    csSel.execute(sqlSel)
    ids = list(csSel.fetchall())
    cntData = len(ids)
    print 'debug[19] cntData = %d' % cntData
    ratio = conf['positiveRatio'] if cls == '1' else conf['counterRatio']
    cntSample = int(cntData * ratio)

    i = 0
    while i < cntSample and cntData != 0:
        seed = randrange(0, cntData)
        sqlSubsel = sqls['selData'] % ids[seed]
        csSubSel.execute(sqlSubsel)
        d = csSubSel.fetchone()
        f.write('%d,%d,%d,%d,%s\n' % (d[0], d[1], d[2], d[3], d[4]))
        isReturn = conf['positiveIsReturn'] if cls == '1' else conf['counterIsReturn']
        if not isReturn:
            del ids[seed]
            cntData = cntData - 1
        stdout.write('debug[39] i = %d\r' % i)
        i = i + 1

def main():
    confPath = path.abspath(argv[1])
    confDir = path.dirname(confPath)
    confName = path.splitext(path.basename(confPath))[0]
    output = '%s/%s' % (confDir, confName)

    f = open(confPath, 'r')
    conf = load(f)
    f.close()
    assert(conf['isTrain'])

    sqls = {'selDataId':selDataId, 'selData':selData} 
    db = connect(database['host'], database['user'], database['password'], database['database'])

    try:
        mkdir(output)
    except WindowsError, err:
        print err

    f = open('%s/%s.csv' % (output, confName), 'w')
    f.write('id,user_id,item_category,item_id,class\n')
    print 'debug[53] positive'
    genTrain(db, sqls, f, '1', conf)
    print 'debug[55] counter'
    genTrain(db, sqls, f, '0', conf)
    f.close()

    db.close()

    copy(confPath, '%s/%s.json' % (output, confName))
    tar = tarfile.open('%s.sample' % output, 'w')
    tar.add(output, arcname=confName) 
    tar.close()
    rmtree(output)

if __name__ == '__main__':
    main()
