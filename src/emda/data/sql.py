delData = 'delete from data'

insData = '''insert into data values(%d, %d, %d, %d, '%s')
'''
selDataId = '''select id
from data where
class = '%s'
'''
selData = '''select * 
from data where 
id = %d
'''

selPredict = '''select * from predict where
user_id = %d and item_id = %d
'''
