from sys import argv
from sys import stdout
from os import path
from json import load

from MySQLdb import connect
from MySQLdb import InternalError

from settings import database

from sql import delData
from sql import insData

def genData(db, sqls, conf):
    csSel = db.cursor()
    csSubSel = db.cursor()
    csDel = db.cursor()
    csIns = db.cursor()


    sqlDel = sqls['delData']
    csDel.execute(sqlDel)

    sqlSel = conf['selUserAndItem']
    csSel.execute(sqlSel)

    i = 1
    while True:
        try:
            (user_id, item_category, item_id) = csSel.fetchone()
        except TypeError, err:
            break
        sqlSubsel = conf['selLabel'] % (user_id, item_id)
        csSubSel.execute(sqlSubsel)
        cls = '1' if csSubSel.fetchone()[0] > 0 else '0'

        sqlIns = sqls['insData'] % (i, user_id, item_category, item_id, cls)
        csIns.execute(sqlIns)

        stdout.write('debug[40] i=%d\r' % i)

        i = i + 1

def main():
    confPath = path.abspath(argv[1])
    confDir = path.dirname(confPath)
    confName = path.splitext(path.basename(confPath))[0]

    f = open(confPath, 'r')
    conf = load(f)
    f.close()
    assert(conf['isTrain'])

    sqls = {'delData':delData, 'insData':insData}

    db = connect(database['host'], database['user'], database['password'], database['database'])


    genData(db, sqls, conf)
    db.commit()

    db.close()

if __name__ == '__main__':
    main()
