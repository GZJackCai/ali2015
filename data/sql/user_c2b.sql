/*
drop table user_c2b;
create table user_c2b
(
begin_time varchar(13),
end_time varchar(13),
user_id integer,
time_count integer,
cart_sum integer,
cart_buy_today_sum integer,
cart_buy_tomorrow_sum integer,
cart_buy_tomorrow_not_cart_tomorrow_sum integer,
cart_not_buy_sum integer,
cart_buy_tomorrow_by_cart_average decimal(8,8),
primary key(begin_time, end_time, user_id));*/

insert into user_c2b
select begin_time, end_time, user_id, sum(1), sum(cart), sum(cart_buy_today), sum(cart_buy_tomorrow), sum(cart_buy_tomorrow_not_cart_tomorrow), sum(cart_not_buy), avg(cart_buy_tomorrow/cart)
from user_time_c2b
group by begin_time, end_time, user_id

/*
select begin_time, end_time, count(*) from user_c2b 
group by begin_time, end_time
*/