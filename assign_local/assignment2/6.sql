.print Question 6 - liyao1
select l.city, l.prov, coalesce(table_from.cnt_from, 0), coalesce(table_to.cnt_to, 0), coalesce(table_e.cnt_e, 0)
from locations l
left outer join
  (select l1.city, count(r_from.src) as cnt_from
  from locations l1, rides r_from
  where l1.lcode=r_from.src group by l1.city) table_from
on table_from.city = l.city
left outer join
  (select l2.city, count(r_to.dst) as cnt_to
  from locations l2, rides r_to
  where l2.lcode=r_to.dst group by l2.city) table_to
on table_to.city = l.city
left outer join
  (select l3.city, count(e.rno) as cnt_e
  from locations l3, enroute e
  where l3.lcode = e.lcode group by l3.city) table_e
on table_e.city = l.city
group by l.city;
