drop table user_geohash_tmp;
create table user_geohash_tmp(
user_id integer,
geohash varchar(7),
c integer);

insert into user_geohash_tmp
(select user_id, substr(user_geohash, 1, 4) as ug, count(*) as c
from user where user_geohash <> ''
group by user_id, ug)

delete from user_geohash_tmp where exists (select 1 from 
(select user_id, max(c) as c from user_geohash_tmp
group by user_id) m
where m.user_id = user_geohash_tmp.user_id
and m.c > user_geohash_tmp.c)

select * from(
select user_id, c, count(*) as dup
from user_geohash_tmp
group by user_id, c) t
where t.dup > 1

delete from user_geohash_tmp 
where user_id in (1778994, 2202055, 8081753, 13313802, 18717485, 20574240, 23261029, 27383944, 31370999, 36061410, 49897559, 56580525, 59660782, 76327598, 84365253, 86295623, 92773427, 98330735, 108042430, 108735864, 114594263, 119778436, 120784777, 133235363, 140351953)

delete from user_geohash;
insert into user_geohash (select user_id, geohash from user_geohash_tmp)

select * from user_geohash

delete from item_geohash;
insert into item_geohash
select distinct item_id, substr(user_geohash, 1, 4) as ug from
user where user_geohash <> ''

select count(*) from item_geohash

select count(*) from user_geohash u where user_id = 14152 and exists(
select 1 from item_geohash i where item_id = 37320317 and i.geohash = u.geohash)

insert into item_geohash
(select i.item_id, substr(i.item_geohash, 1, 4)
from item i 
where item_geohash <> ''
and not exists (select 1 from item_geohash ig
where ig.item_id = i.item_id and substr(i.item_geohash, 1, 4) = ig.geohash))