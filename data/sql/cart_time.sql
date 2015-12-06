set @begin_time='2014-12-18 00';
set @end_time='2014-12-18 23';
set @behavior_type='4';
/*
drop table cart_time;
create table cart_time
(begin_time varchar(13),
end_time varchar(13),
user_id integer,
item_id integer,
type varchar(1),
behavior_type varchar(1),
before_first_time varchar(13),
after_last_time varchar(13),
primary key(begin_time, end_time, user_id, item_id, type, behavior_type));*/

insert into cart_time
select begin_time, end_time, user_id, item_id, '1', @behavior_type, 
(select min(time) from user u where u.user_id = c_l_d.user_id and u.behavior_type = @behavior_type 
and u.item_category = c_l_d.item_category and u.item_id <> c_l_d.item_id
and u.time >= c_l_d.begin_time and u.time < c_l_d.first_time),
(select max(time) from user u where u.user_id = c_l_d.user_id and u.behavior_type = @behavior_type 
and u.item_category = c_l_d.item_category and u.item_id <> c_l_d.item_id
and u.time > c_l_d.last_time and u.time <= c_l_d.end_time)
from cart_last_day c_l_d
where begin_time = @begin_time and end_time = @end_time;

insert into cart_time
select begin_time, end_time, user_id, item_id, '2', @behavior_type, 
(select min(time) from user u where u.user_id = c_l_d.user_id and u.behavior_type = @behavior_type 
and u.item_id = c_l_d.item_id
and u.time >= c_l_d.begin_time and u.time < c_l_d.first_time),
(select max(time) from user u where u.user_id = c_l_d.user_id and u.behavior_type = @behavior_type 
and u.item_id = c_l_d.item_id
and u.time > c_l_d.last_time and u.time <= c_l_d.end_time)
from cart_last_day c_l_d  
where begin_time = @begin_time and end_time = @end_time;
/*
select begin_time, end_time, type, behavior_type, count(*) from cart_time
group by begin_time, end_time, type, behavior_type*/


