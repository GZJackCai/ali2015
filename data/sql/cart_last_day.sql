set @begin_time='2014-12-10 00';
set @end_time='2014-12-10 23';
/*
drop table cart_last_day;
create table cart_last_day
(begin_time varchar(13),
end_time varchar(13),
user_id integer,
item_category integer,
item_id integer,
first_time varchar(13),
last_time varchar(13),
primary key(begin_time, end_time, user_id, item_id));*/

insert into cart_last_day
select @begin_time, @end_time, user_id, item_category, item_id, min(time), max(time)
from user where time between @begin_time and @end_time and behavior_type = '3'
group by user_id, item_id, behavior_type
order by user_id, item_id, behavior_type;

/*
select begin_time, end_time, count(*) from cart_last_day
group by begin_time, end_time*/
