.print Question 10 - liyao1
select ri.*, r.driver, strftime('%J','2019-01-01') - strftime('%J',ri.rdate)
from ride_info ri, rides r
where ri.rno = r.rno
and ri.src = 'Edmonton' and ri.dst = 'Calgary'
and strftime('%Y-%m', ri.rdate) = '2018-12'
and ri.available > 0
order by ri.price;
