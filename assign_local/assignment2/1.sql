.print Question 1 - liyao1
select distinct name, email
from members, cars c1, cars c2, rides
where email = c1.owner
and c1.owner = c2.owner
and c1.cno <> c2.cno
and (rides.cno = c1.cno OR rides.cno = c2.cno);
