select count(distinct u1.user_id, u1.item_id) from user u1 where u1.time like '2014-12-18 __' and behavior_type = '4'
and 
(exists (select 1 from user u2
--select count(distinct u2.item_id) from user u2
where u2.time between '2014-12-17 00' and '2014-12-17 23' and behavior_type in ('3', '4')
and u2.item_id = u1.item_id)
or
exists (select 1 from user u2
--select count(distinct u2.user_id) from user u2
where u2.time between '2014-12-17 00' and '2014-12-17 23' and behavior_type in ('4')
and u2.user_id = u1.user_id))

select count(distinct u2.item_id) from user u2
where u2.time between '2014-12-17 00' and '2014-12-17 23' and behavior_type in ('3', '4')
and exists (select 1 from item i
where i.item_id = u2.item_id)

select count(distinct u2.user_id) from user u2
where u2.time between '2014-12-17 00' and '2014-12-17 23' and behavior_type in ('4')