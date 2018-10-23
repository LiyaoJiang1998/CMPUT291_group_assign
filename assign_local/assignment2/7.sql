.print Question 7 - liyao1
select rides.rno
from rides, locations ls, locations ld
where rides.src = ls.lcode and rides.dst = ld.lcode
and ls.city = 'Edmonton' and ld.city = 'Calgary'
and strftime('%Y-%m', rides.rdate) = '2018-10'
and rides.seats > (
  select coalesce(sum(bookings.seats),0)
  from bookings
  where bookings.rno = rides.rno
)
and rides.price = (
  select min(rides.price)
  from rides, locations ls, locations ld
  where rides.src = ls.lcode and rides.dst = ld.lcode
  and ls.city = 'Edmonton' and ld.city = 'Calgary'
  and strftime('%Y-%m', rides.rdate) = '2018-10'
  and rides.seats > (
    select coalesce(sum(bookings.seats),0)
    from bookings
    where bookings.rno = rides.rno
  )
);
