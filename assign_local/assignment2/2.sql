.print Question 2 - liyao1
select name, members.email
from members, cars, bookings
where members.email = owner
and members.email = bookings.email
except
select name, email
from members, rides
where email = driver;
