set @begin_time='2014-11-19 00';
set @cart_end_time = '2014-12-16 23';
set @except_begin_time = '2014-12-11 00';
set @except_end_time = '2014-12-12 03';
set @end_time='2014-12-18 23';

/*
drop table user_active_cart;
create table user_active_cart(
begin_time varchar(13),
end_time varchar(13),
user_id integer,
time varchar(13),
primary key(begin_time, end_time, user_id, time));*/

insert into user_active_cart
select distinct @begin_time, @end_time, user_id, substr(time, 1, 10) as t from user where behavior_type = '3'
and time between @begin_time and @end_time
and time between @begin_time and @cart_end_time
and time not between @except_begin_time and @except_end_time

/*
select begin_time, end_time, count(*) from user_active_cart
group by begin_time, end_time*/
