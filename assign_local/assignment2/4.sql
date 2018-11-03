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
