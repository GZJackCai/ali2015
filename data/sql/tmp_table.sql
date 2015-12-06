drop table user_group;
create table user_group
(
type varchar(1),
user_id integer,
behavior_type varchar(1),
begin_time varchar(13),
end_time varchar(13),
count integer,
primary key(type, user_id, behavior_type, begin_time, end_time));
--conditions
insert into user_group 
select '2', user_id, behavior_type, '2014-12-17 00', '2014-12-17 23', count(distinct substr(time, 1, 10))
from user where behavior_type = '1' and time between '2014-12-17 00' and '2014-12-17 23'
group by user_id, behavior_type/*
drop table category_group;
create table category_group
(
type varchar(1),
item_category integer,
behavior_type varchar(1),
begin_time varchar(13),
end_time varchar(13),
count integer,
primary key(type, item_category, behavior_type, begin_time, end_time));*/
--conditions
/*
insert into category_group 
select '1' as type, item_category, behavior_type, '2014-12-15 00', '2014-12-17 23', count(substr(time, 1, 10))
from user where behavior_type = '3' and time between '2014-12-15 00' and '2014-12-17 23'
group by item_category, behavior_type*/


