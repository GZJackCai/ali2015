set @buy_begin_time = '2014-11-19 00';
set @buy_end_time = '2014-12-18 23';
set @begin_time = '2014-12-18 00';
set @end_time = '2014-12-18 23';

/*
drop table cart_buy;
create table cart_buy
(begin_time varchar(13),
end_time varchar(13),
user_id integer,
item_category integer,
item_id integer,
buy_count integer,
primary key(begin_time, end_time, user_id, item_id));

drop table cart_buy_max_in_user;
create table cart_buy_max_in_user
(begin_time varchar(13),
end_time varchar(13),
user_id integer,
buy_max integer,
primary key(begin_time, end_time, user_id));

drop table cart_buy_max_in_user_category;
create table cart_buy_max_in_user_category
(begin_time varchar(13),
end_time varchar(13),
user_id integer,
item_category integer,
buy_max integer,
primary key(begin_time, end_time, user_id, item_category));*/


insert into cart_buy
select begin_time, end_time, user_id, item_category, item_id, 
(select count(*) from user u where behavior_type = '4'
and u.item_id = c_l_d.item_id and time between @buy_begin_time and @buy_end_time)
from cart_last_day c_l_d
where begin_time = @begin_time and end_time = @end_time;

/*
insert into cart_buy_max_in_user
select begin_time, end_time, user_id, 
max(buy_count)
from cart_buy c_b_1
group by begin_time, end_time, user_id;

insert into cart_buy_max_in_user_category
select begin_time, end_time, user_id, item_category,
max(buy_count)
from cart_buy c_b_1
group by begin_time, end_time, user_id, item_category;*/

/*
select begin_time, end_time, count(*) from cart_buy
group by begin_time, end_time*/
