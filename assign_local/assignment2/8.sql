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
