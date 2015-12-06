drop index idx_user1 on user;
drop index idx_user2 on user;
drop index idx_user3 on user;
drop index idx_user4 on user;
drop table user;
create table user(
user_id integer,
item_id integer,
behavior_type varchar(1),
user_geohash varchar(7),
item_category integer,
time varchar(13));
create index idx_user1 on user(user_id);
create index idx_user2 on user(item_id);
create index idx_user3 on user(user_id, item_id);
create index idx_user4 on user(item_category);

drop index idx_item on item;
drop table item;
create table item(
item_id integer,
item_geohash varchar(7),
item_category integer);
create index idx_item on item(item_id);

drop table data;
create table data(
id integer,
user_id integer,
item_category integer,
item_id integer,
class varchar(1),
primary key(id));

drop table user_id;
create table user_id
(user_id integer,
primary key(user_id));
insert into user_id
select distinct user_id from user;

drop table item_id;
create table item_id
(item_id integer,
item_category integer,
primary key(item_id, item_category));
insert into item_id
select distinct item_id, item_category from user;

drop table item_category;
create table item_category
(item_category integer,
primary key(item_category));
insert into item_category
select distinct item_category from user;

drop table user_geohash;
create table user_geohash(
user_id integer,
geohash varchar(7),
primary key(user_id, geohash));

drop table item_geohash;
create table item_geohash(
item_id integer,
geohash varchar(7),
count integer,
primary key(item_id, geohash));


drop table predict;
create table predict(
user_id integer,
item_id integer,
class varchar(1),
primary key(user_id, item_id));

