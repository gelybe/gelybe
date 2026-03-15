-- select * from table_1;
-- select * from table_2;

-- select * from table_1 inner join table_2 on table_1.first_name = table_2.first_name;

-- select table_1.first_name, table_1.last_name, born_city,
--        table_2.first_name, table_2.last_name, born_country
-- from table_1
-- inner join table_2
-- on table_1.first_name = table_2.first_name;

-- select table_1.first_name as t1_first_name,
--        table_2.first_name as t2_first_name,
--        count(*) as similarities
-- from table_1
-- inner join table_2
-- on table_1.first_name = table_2.first_name
-- group by table_1.first_name, table_2.first_name
-- order by COUNT(table_1.first_name == table_2.first_name) desc;

-- select *
-- from table_1
-- left outer join table_2
-- on table_1.first_name == table_2.first_name;

-- select *
-- from table_2
-- left outer join table_1
-- on table_1.first_name == table_2.first_name;

-- select *
-- from table_1
-- left outer join table_2
-- on table_1.first_name == table_2.first_name
-- where table_2.first_name is null;

-- select first_name from table_1
-- union
-- select first_name from table_2;


select first_name from table_1
union all
select first_name from table_2;