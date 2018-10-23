.echo on

--Question 1
.print Question 1 - liyao1
select distinct name, email
from members, cars c1, cars c2, rides
where email = c1.owner
and c1.owner = c2.owner
and c1.cno <> c2.cno
and (rides.cno = c1.cno OR rides.cno = c2.cno);

--Question 2
.print Question 2 - liyao1
select name, members.email
from members, cars, bookings
where members.email = owner
and members.email = bookings.email
except
select name, email
from members, rides
where email = driver;

--Question 3
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

--Question 4
.print Question 4 - liyao1
select requests.rid, requests.email, ls_req.lcode, ld_req.lcode, rides.rno
from requests, rides, locations ls_ride, locations ld_ride,
     locations ls_req, locations ld_req
where requests.rdate = rides.rdate
and rides.price <= requests.amount
and rides.src = ls_ride.lcode and rides.dst = ld_ride.lcode
and requests.pickup = ls_req.lcode and requests.dropoff = ld_req.lcode
and ls_req.city = ls_ride.city and ld_req.city = ld_ride.city
and ls_req.prov = ls_ride.prov and ld_req.prov = ld_ride.prov;

--Question 5
.print Question 5 - liyao1
select l.city, l.prov
from locations l, rides r
where r.dst = l.lcode
group by l.city, l.prov
order by count(*) desc
limit 3;

--Question 6
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

--Question 7
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

--Question 8
.print Question 8 - liyao1
select members.email
from members
where (select count(rides.rno)
      from rides, locations ld
      where members.email = rides.driver
      and rides.dst = ld.lcode and ld.prov = 'Alberta'
      and strftime('%Y', rides.rdate) >= '2016'
      group by rides.driver
      ) >
        (select cast(count(*) as float)/2
        from locations
        where locations.prov = 'Alberta'
        )
except
select rides.driver
from rides
where strftime('%Y', rides.rdate) < '2016';

--Question 9
.print Question 9 - liyao1
create view ride_info(rno, booked, available, rdate, price, src, dst)
  as
  select r.rno, coalesce(sum(b.seats),0), r.seats-coalesce(sum(b.seats),0),
         r.rdate, r.price, ls.city, ld.city
  from rides r left outer join bookings b on b.rno = r.rno, locations ls, locations ld
  where ls.lcode = r.src and ld.lcode = r.dst
  and r.rdate > datetime('now')
  group by r.rno, r.seats, r.rdate, r.price, ls.city, ld.city;

--Question 10
.print Question 10 - liyao1
select ri.*, r.driver, strftime('%J','2019-01-01') - strftime('%J',ri.rdate)
from ride_info ri, rides r
where ri.rno = r.rno
and ri.src = 'Edmonton' and ri.dst = 'Calgary'
and strftime('%Y-%m', ri.rdate) = '2018-12'
and ri.available > 0
order by ri.price;
