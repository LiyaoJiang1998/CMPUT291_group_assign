.print Question 9 - liyao1
create view ride_info(rno, booked, available, rdate, price, src, dst)
  as
  select r.rno, coalesce(sum(b.seats),0), r.seats-coalesce(sum(b.seats),0),
         r.rdate, r.price, ls.city, ld.city
  from rides r left outer join bookings b on b.rno = r.rno, locations ls, locations ld
  where ls.lcode = r.src and ld.lcode = r.dst
  and r.rdate > datetime('now')
  group by r.rno, r.seats, r.rdate, r.price, ls.city, ld.city;
