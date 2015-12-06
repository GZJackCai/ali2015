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
    csUser_p = c.cursor()
    csUser_c = c.cursor()
    csUpt = c.cursor()

    sqlUser_id = '''select user_id from user_id'''
    csUser_id.execute(sqlUser_id)


    while True:
        user_id = csUser_id.fetchone()
        if not user_id:
            break

        print 'debug[27] user_id = %d' % user_id

        sqlUser_p = '''select user_id, item_id, behavior_type, item_category, time, substr(user_geohash, 1, 5)
from user where
user_id = %d and time <= '%s 23' and user_geohash <> ''
''' % (user_id[0], argv[1])
        sqlUser_c = '''select user_id, item_id, behavior_type, item_category, time, substr(user_geohash, 1, 5)
from user where
user_id = %d and time <= '%s 23' and user_geohash = ''
''' % (user_id[0], argv[1])


        csUser_p.execute(sqlUser_p)
        actions = csUser_p.fetchall()
        cntActions = len(actions)
        if cntActions == 0:
            continue

        trainSet_x = []
        trainSet_y = []
        for i in range(cntActions):
            t = datetime.strptime(actions[i][4], '%Y-%m-%d %H')
            trainSet_x.append([str(actions[i][1]), actions[i][2], str(actions[i][3])] + [t.month, t.day, t.hour, t.weekday()] + list(actions[i][6:-1]))
            trainSet_y.append(actions[i][-1])
            
        trainSet_x = array(trainSet_x)
        trainSet_y = array(trainSet_y)
        #clf = GradientBoostingClassifier()
        clf = RandomForestClassifier()
        clf.fit(trainSet_x, trainSet_y)

        csUser_c.execute(sqlUser_c)
        actions = csUser_c.fetchall()
        cntActions = len(actions)
        if cntActions == 0:
            continue

        for i in range(cntActions):
            t = datetime.strptime(actions[i][4], '%Y-%m-%d %H')
            sample = array([str(actions[i][1]), actions[i][2], str(actions[i][3])] + [t.month, t.day, t.hour, t.weekday()] + list(actions[i][6:-1]))
            geohash = clf.predict(sample)[0]
            #print 'debug[71] sample = %s' % str(sample)
            #print 'debug[72] geohash = %s' % geohash
            sqlUpt = '''update user set user_geohash = '%s__' where
user_id = %d and item_id = %d and behavior_type = '%s' and user_geohash = '' and item_category = %d and
time = '%s'
''' % (geohash, actions[i][0], actions[i][1], actions[i][2], actions[i][3], actions[i][4])
            #print 'debug[54] sqlUpt = %s' % sqlUpt
            csUpt.execute(sqlUpt)
            #raw_input()

    c.commit()
    c.close()

if __name__ == '__main__':
    main()
