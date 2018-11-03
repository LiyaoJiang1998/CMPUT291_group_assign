.print Question 3 - liyao1
select distinct members.email
from members, rides, bookings, locations ls , locations ld
where members.email = bookings.email
and rides.rno = bookings.rno
and src = ls.lcode
and dst = ld.lcode
and ls.city = 'Edmonton'
and ld.city = 'Calgary'
and strftime('%Y-%m', rdate) = '2018-11';
