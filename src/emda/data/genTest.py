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

from sql import selPredict

def genTest(db, sqls, f, conf):
    csSelUser = db.cursor()
    csSelItem = db.cursor()
    csSelPredict = db.cursor()

    sqlSelUser = conf['selUser']
    sqlSelItem = conf['selItem']

    csSelUser.execute(sqlSelUser)
    users = list(csSelUser.fetchall())
    print 'debug[27] cntUser = %d' % len(users)

    csSelItem.execute(sqlSelItem)
    items = list(csSelItem.fetchall())
    print 'debug[27] cntItem = %d' % len(items)

    i = 0
    lastUserId = -1
    for user in users:
        if user[0] != lastUserId:
            itemOfUser = []
        for item in items:
            if user[1] != item[2]:
                continue
            if item[0] in itemOfUser:
                #print 'debug[41] ignore duplicate, user_id = %d' % user[0]
                continue
            sqlSelPredict = sqls['selPredict'] % (user[0], item[0])
            csSelPredict.execute(sqlSelPredict)
            if csSelPredict.fetchone():
                continue
            f.write('%d,%d,%d,%d,%s\n' % (i, user[0], item[1], item[0], '?'))
            itemOfUser.append(item[0])
            stdout.write('debug[32] i = %d\r' % i)
            i = i + 1
        lastUserId = user[0]

def main():
    sqls = {'selPredict':selPredict}

    confPath = path.abspath(argv[1])
    confDir = path.dirname(confPath)
    confName = path.splitext(path.basename(confPath))[0]
    output = '%s/%s' % (confDir, confName)

    f = open(confPath, 'r')
    conf = load(f)
    f.close()
    assert(not conf['isTrain'])

    db = connect(database['host'], database['user'], database['password'], database['database'])

    try:
        mkdir(output)
    except WindowsError, err:
        print err

    f = open('%s/%s.csv' % (output, confName), 'w')
    f.write('id,user_id,item_category,item_id,class\n')
    genTest(db, sqls, f, conf)
    f.close()

    db.close()

    copy(confPath, '%s/%s.json' % (output, confName))
    tar = tarfile.open('%s.sample' % output, 'w')
    tar.add(output, arcname=confName) 
    tar.close()
    rmtree(output)

if __name__ == '__main__':
    main()
