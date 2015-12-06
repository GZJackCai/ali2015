--select * from predict where class = '1' 
--select * from todo

select count(*) from predict p where 
p.class = '1' and 
exists(
select 1 from user u where 
u.user_id = p.user_id and u.item_id = p.item_id and 
--select count(*) from user u where
u.behavior_type = '4' and u.time like '2014-12-18 __'
and exists(
select 1 from item i where
i.item_id = u.item_id))
/*
select count(*) from todo td
where exists (select 1 from predict p where
p.user_id = td.user_id and p.item_id = td.item_id and p.class = '1')*/