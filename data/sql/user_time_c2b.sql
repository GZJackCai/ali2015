/*
drop table user_time_c2b;
create table user_time_c2b
(
begin_time varchar(13),
end_time varchar(13),
user_id integer,
time varchar(13),
cart integer,
cart_buy_today integer,
cart_buy_tomorrow integer,
cart_buy_tomorrow_not_cart_tomorrow integer,
cart_not_buy integer,
primary key(begin_time, end_time, user_id, time));*/

insert into user_time_c2b
select begin_time, end_time, user_id, time,
(select count(*) from user u1 where u1.user_id = u_a_c.user_id and substr(time, 1, 10) = u_a_c.time and behavior_type = '3') as cart,

(select count(*) from user u1 where u1.user_id = u_a_c.user_id and substr(time, 1, 10) = u_a_c.time and behavior_type = '3'
and exists(select 1 from user u2 where
u2.user_id = u1.user_id and u2.item_id = u1.item_id and substr(u1.time, 1, 10) = substr(u2.time, 1, 10) and behavior_type = '4')) as cart_buy_today,

(select count(*) from user u1 where u1.user_id = u_a_c.user_id and substr(time, 1, 10) = u_a_c.time and behavior_type = '3'
and not exists(select 1 from user u2 where
u2.user_id = u1.user_id and u2.item_id = u1.item_id and substr(u1.time, 1, 10) = substr(u2.time, 1, 10) and behavior_type = '4')
and exists(select 1 from user u2 where
u2.user_id = u1.user_id and u2.item_id = u1.item_id and datediff(substr(u1.time, 1, 10), substr(u2.time, 1, 10)) = -1 and behavior_type = '4' and time between u_a_c.begin_time and u_a_c.end_time)
) as cart_buy_tomorrow,

(select count(*) from user u1 where u1.user_id = u_a_c.user_id and substr(time, 1, 10) = u_a_c.time and behavior_type = '3'
--not buy today
and not exists(select 1 from user u2 where
u2.user_id = u1.user_id and u2.item_id = u1.item_id and substr(u1.time, 1, 10) = substr(u2.time, 1, 10) and behavior_type = '4')
--buy tomorrow
and exists(select 1 from user u2 where
u2.user_id = u1.user_id and u2.item_id = u1.item_id and datediff(substr(u1.time, 1, 10), substr(u2.time, 1, 10)) = -1 and behavior_type = '4' and time between u_a_c.begin_time and u_a_c.end_time)
--not cart tomorrow
and not exists(select 1 from user u2 where
u2.user_id = u1.user_id and u2.item_id = u1.item_id and datediff(substr(u1.time, 1, 10), substr(u2.time, 1, 10)) = -1 and behavior_type = '3' and time between u_a_c.begin_time and u_a_c.end_time)
) as cart_buy_tomorrow_not_cart_tomorrow,

(select count(*) from user u1 where u1.user_id = u_a_c.user_id and substr(time, 1, 10) = u_a_c.time and behavior_type = '3'
and not exists(select 1 from user u2 where
u2.user_id = u1.user_id and u2.item_id = u1.item_id and u2.time >= u1.time and behavior_type = '4' and time between u_a_c.begin_time and u_a_c.end_time)) as cart_not_buy
from user_active_cart u_a_c

/*
select begin_time, end_time, count(*) from user_time_c2b 
group by begin_time, end_time
*/