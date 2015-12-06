set @begin_time='2014-12-16 00';
set @end_time='2014-12-16 23';
/*
drop table cart_group;
create table cart_group
(begin_time varchar(13),
end_time varchar(13),
user_id integer,
item_id integer,
behavior_type varchar(1),
before_count integer,
between_count integer,
after_count integer,
primary key(begin_time, end_time, user_id, item_id, behavior_type));*/

delete from cart_group where begin_time = @begin_time and end_time = @end_time;
insert into cart_group
select begin_time, end_time, user_id, item_id, behavior_type, 
(select count(*) from user u where u.behavior_type = c_l_d.behavior_type and u.time >= c_l_d.begin_time and u.time < c_l_d.first_time),
(select count(*) from user u where u.behavior_type = c_l_d.behavior_type and u.time >= c_l_d.first_time and u.time <= c_l_d.last_time),
(select count(*) from user u where u.behavior_type = c_l_d.behavior_type and u.time > c_l_d.last_time and u.time <= c_l_d.end_time)
from cart_last_day c_l_d  
where begin_time = @begin_time and @end_time = @end_time;

/*
select * from cart_group*/


