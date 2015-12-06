delete from item_geohash;
insert into item_geohash
select item_id, substr(user_geohash, 1, 5) as ug , count(*)
from user where user_geohash <> ''
group by item_id, ug;

select count(distinct item_id) from item_geohash;

insert into item_geohash
(select distinct i.item_id, substr(i.item_geohash, 1, 5),  0
from item i 
where item_geohash <> ''
and not exists (select 1 from item_geohash ig
where ig.item_id = i.item_id and substr(i.item_geohash, 1, 5) = ig.geohash));