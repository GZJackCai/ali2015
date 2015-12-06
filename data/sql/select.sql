select count(distinct item_id) from item
select count(distinct item_id) from user
select count(distinct user_id) from user
select count(distinct user_id, item_id) from user
where behavior_type = '4' and time like '2014-12-18%'
select count(distinct item_category) from user
select count(distinct user_id, item_id) from user where 
time between '2014-12-18 00' and '2014-12-18 23' 

select user_geohash from user

select count(distinct user_id, item_id) from ali_raw.user u1
where behavior_type = '4' and time like '2014-12-17%'
and not exists (select 1 from ali_raw.user u2 where u2.user_id = u1.user_id 
//and u2.item_id = u1.item_id
and u2.time < '2014-12-17 00'

select min(item_category), max(item_category) from user

select u.user_id, i.item_id
from
(select distinct user_id from ali_raw.user) u,
(select distinct item_id from ali_raw.item) i

select count(distinct user.item_id) from user
where not exists
(select 1 from item where item.item_id = user.item_id)

select count(distinct item.item_id) from item
where not exists
(select 1 from user where user.item_id = item.item_id) 

select count(*) from data where class = '1'


select count(distinct item_id) from user 
where behavior_type in ('4')

select count(distinct u1.item_id) from user u1
where u1.behavior_type = '4' and u1.time >= '2014-12-12 00'
and not exists (select 1 from user u2 where u2.item_id = u1.item_id and u2.time < '2014-12-12 00')


select count(distinct user_id) from user where time between '2014-12-12 00' and '2014-12-18 23' and behavior_type in ('3', '4')

select count(distinct u.item_id) from user u 
where u.time between '2014-12-12 00' and '2014-12-18 23' and u.behavior_type in ('3', '4')
and exists (select 1 from item i where i.item_id = u.item_id)