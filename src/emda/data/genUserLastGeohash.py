from sys import argv

from MySQLdb import connect
from datetime import datetime
from numpy import array
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier

from settings import database

def main():
    c = connect(database['host'], database['user'], database['password'], database['database'])

    csUser_id = c.cursor()
    csUser = c.cursor()
    csDelete = c.cursor()
    csInsert = c.cursor()

    sqlDelete = '''delete from user_geohash'''
    csDelete.execute(sqlDelete)

    sqlUser_id = '''select user_id from user_id'''
    csUser_id.execute(sqlUser_id)

    while True:
        user_id = csUser_id.fetchone()
        if not user_id:
            break

        print 'debug[27] user_id = %d' % user_id

        sqlUser= '''select substr(time, 1, 10) as t
from user where
user_id = %d and user_geohash <> '' and time <= '%s 23'
order by t desc
limit 1
''' % (user_id[0], argv[1])

        csUser.execute(sqlUser)
        lastDay = csUser.fetchone()
        if not lastDay:
            continue

        sqlInsert = '''insert into user_geohash
select distinct user_id, substr(user_geohash, 1, 5)
from user where
user_id = %d and time like '%s __'
''' % (user_id[0], lastDay[0])

        csInsert.execute(sqlInsert)

    c.commit()
    c.close()

if __name__ == '__main__':
    main()
