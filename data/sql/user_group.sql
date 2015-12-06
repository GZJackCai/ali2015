set @bgnDate='2014-12-08 00';
set @endDate='2014-12-08 23';
set @behavior_type='4';

/*drop table user_group;
create table user_group
(
type varchar(1),
user_id integer,
behavior_type varchar(1),
begin_time varchar(13),
end_time varchar(13),
count integer,
primary key(type, user_id, behavior_type, begin_time, end_time));*/
--conditions

insert into user_group 
select '1', user_id, behavior_type, @bgnDate, @endDate, count(*)
from user where behavior_type = @behavior_type and time between @bgnDate and @endDate
group by user_id, behavior_type;

insert into user_group 
select '2', user_id, behavior_type, @bgnDate, @endDate, count(distinct substr(time, 1, 10))
from user where behavior_type = @behavior_type and time between @bgnDate and @endDate
group by user_id, behavior_type;

insert into user_group 
select '3', user_id, behavior_type, @bgnDate, @endDate, count(distinct item_category)
from user where behavior_type = @behavior_type and time between @bgnDate and @endDate
group by user_id, behavior_type;
/*
select type, behavior_type, begin_time, end_time, count(*)
from user_group
group by type, behavior_type, begin_time, end_time*/