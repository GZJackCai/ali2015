set @begin_time='2014-12-18 00';
set @end_time='2014-12-18 23';
set @a_begin_time='2014-11-19 00';
set @a_end_time='2014-12-18 23';
set @behavior_type='4';
/*
drop table cart_max;
create table cart_max
(begin_time varchar(13),
end_time varchar(13),
user_id integer,
item_id integer,
type varchar(1),
behavior_type varchar(1),
which varchar(1),
max_user_item integer,
max_item integer,
primary key(begin_time, end_time, user_id, item_id, type, behavior_type, which));*/

insert into cart_max
select begin_time, end_time, user_id, item_id, type, @behavior_type, which, max(user_item_count), max(item_count) from(
select begin_time, end_time, user_id, item_id, type, @behavior_type, which,
ifnull((select count from user_item_group u_i_g where u_i_g.type = '1'
and u_i_g.user_id = c_i.user_id and u_i_g.item_id = c_i.which_item_id and u_i_g.behavior_type = @behavior_type
and u_i_g.begin_time = @a_begin_time and u_i_g.end_time = @a_end_time), 0) as user_item_count,
ifnull((select count from item_group i_g where i_g.type = '1'
and i_g.item_id = c_i.which_item_id and i_g.behavior_type = @behavior_type
and i_g.begin_time = @a_begin_time and i_g.end_time = @a_end_time), 0) as item_count
from cart_item c_i
where begin_time = @begin_time and end_time = @end_time) t
group by begin_time, end_time, user_id, item_id, type, which

/*
select begin_time, end_time, type, behavior_type, which, count(*) from cart_max
group by begin_time, end_time, type, behavior_type, which*/