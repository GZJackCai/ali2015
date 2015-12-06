set @begin_time='2014-12-17 00';
set @end_time='2014-12-17 23';
/*
drop table cart_item;
create table cart_item
(begin_time varchar(13),
end_time varchar(13),
user_id integer,
item_id integer,
type varchar(1),
which varchar(1),
which_item_id integer,
primary key(begin_time, end_time, user_id, item_id, type, which, which_item_id));*/

insert into cart_item
select distinct c_l_d.begin_time, c_l_d.end_time, c_l_d.user_id, c_l_d.item_id, '1', '0', u.item_id
from cart_last_day c_l_d, user u
where c_l_d.begin_time = @begin_time and c_l_d.end_time = @end_time
and c_l_d.user_id = u.user_id
and c_l_d.item_category = u.item_category and c_l_d.item_id <> u.item_id
and u.time >= c_l_d.begin_time and u.time < c_l_d.first_time;

insert into cart_item
select distinct c_l_d.begin_time, c_l_d.end_time, c_l_d.user_id, c_l_d.item_id, '1', '1', u.item_id
from cart_last_day c_l_d, user u
where c_l_d.begin_time = @begin_time and c_l_d.end_time = @end_time
and c_l_d.user_id = u.user_id
and c_l_d.item_category = u.item_category and c_l_d.item_id <> u.item_id
and u.time >= c_l_d.first_time and u.time <= c_l_d.last_time;

insert into cart_item
select distinct c_l_d.begin_time, c_l_d.end_time, c_l_d.user_id, c_l_d.item_id, '1', '2', u.item_id
from cart_last_day c_l_d, user u
where c_l_d.begin_time = @begin_time and c_l_d.end_time = @end_time
and c_l_d.user_id = u.user_id
and c_l_d.item_category = u.item_category and c_l_d.item_id <> u.item_id
and u.time > c_l_d.last_time and u.time <= c_l_d.end_time;


insert into cart_item
select distinct c_l_d.begin_time, c_l_d.end_time, c_l_d.user_id, c_l_d.item_id, '2', '0', u.item_id
from cart_last_day c_l_d, user u
where c_l_d.begin_time = @begin_time and c_l_d.end_time = @end_time
and c_l_d.user_id = u.user_id
and c_l_d.item_id = u.item_id
and u.time >= c_l_d.begin_time and u.time < c_l_d.first_time;

insert into cart_item
select distinct c_l_d.begin_time, c_l_d.end_time, c_l_d.user_id, c_l_d.item_id, '2', '1', u.item_id
from cart_last_day c_l_d, user u
where c_l_d.begin_time = @begin_time and c_l_d.end_time = @end_time
and c_l_d.user_id = u.user_id
and c_l_d.item_id = u.item_id
and u.time >= c_l_d.first_time and u.time <= c_l_d.last_time;

insert into cart_item
select distinct c_l_d.begin_time, c_l_d.end_time, c_l_d.user_id, c_l_d.item_id, '2', '2', u.item_id
from cart_last_day c_l_d, user u
where c_l_d.begin_time = @begin_time and c_l_d.end_time = @end_time
and c_l_d.user_id = u.user_id
and c_l_d.item_id = u.item_id
and u.time > c_l_d.last_time and u.time <= c_l_d.end_time;

/*
select * from cart_item/