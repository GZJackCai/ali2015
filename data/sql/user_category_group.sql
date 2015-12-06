set @bgnDate='2014-11-25 00';
set @endDate='2014-12-09 23';
set @behavior_type='4';

/*drop table user_category_group;
create table user_category_group
(
type varchar(1),
user_id integer,
item_category integer,
behavior_type varchar(1),
begin_time varchar(13),
end_time varchar(13),
count integer,
primary key(type, user_id, item_category, behavior_type, begin_time, end_time));*/
--conditions

insert into user_category_group 
select '1', user_id, item_category, behavior_type, @bgnDate, @endDate, count(*)
from user where behavior_type = @behavior_type and time between @bgnDate and @endDate
group by user_id, item_category, behavior_type
/*
select type, behavior_type, begin_time, end_time, count(*)
from user_category_group
group by type, behavior_type, begin_time, end_time*/