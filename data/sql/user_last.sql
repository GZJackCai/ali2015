set @behavior_type='4';
set @begin_time='2014-11-18 00';
set @end_time='2014-12-17 23';

/*
drop table user_last;
create table user_last
(
user_id integer,
behavior_type varchar(1),
begin_time varchar(13),
end_time varchar(13),
datediff integer,
primary key(user_id, behavior_type, begin_time, end_time));*/

insert into user_last
select user_id, @behavior_type, @begin_time, @end_time,
ifnull((select datediff(substr(@end_time, 1, 10), substr(u.time, 1, 10)) from user u
where behavior_type = @behavior_type
and u.user_id = u_i.user_id
and u.time between @before_time and @end_time
order by time desc
limit 1), 45)
from user_id u_i;

/*
select behavior_type, begin_time, end_time, count(*) from user_last
group by behavior_type, begin_time, end_time*/