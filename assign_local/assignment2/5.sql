.print Question 5 - liyao1
select l.city, l.prov
from locations l, rides r
where r.dst = l.lcode
group by l.city, l.prov
order by count(*) desc
limit 3;
