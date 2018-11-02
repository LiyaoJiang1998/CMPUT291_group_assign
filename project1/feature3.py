'''
Book members or cancel bookings.The member should be able to list all bookings
on rides s/he offers and cancel any booking. For any booking that is cancelled
(i.e. being deleted from the booking table), a proper message should be sent to
the member whose booking is cancelled. Also the member should be able to book
other members on the rides they offer.

Your system should list all rides the
member offers with the number of available seats for each ride (i.e., seats that
 are not booked). If there are more than 5 matching rides, at most 5 will be
shown at a time, and the member will have the option to see more.

The member
should be able to select a ride and book a member for that ride by entering the
member email, the number of seats booked, the cost per seat, and pickup and drop
 off location codes. Your system should assign a unique booking number (bno) to
the booking. Your system should give a warning if a ride is being overbooked
(i.e. the number of seats booked exceeds the number of seats offered), but will
allow overbooking if the member confirms it. After a successful booking, a
proper message should be sent to the other member that s/he is booked on the ride.
'''

import sqlite3

# conn = sqlite3.connect('./project1.db')

def listAllRides(conn, c, email):
    '''
    list all the rides the member offers with # of available seats
    '''

    # create a view about each ride
    c.execute('''
        drop view if exists ride_info;
        ''')
    c.execute('''
        create view ride_info(driver, rno, booked, available, rdate, price, src, dst)
        as
        select r.driver, r.rno, coalesce(sum(b.seats),0), r.seats-coalesce(sum(b.seats),0),
             r.rdate, r.price, ls.city, ld.city
        from rides r left outer join bookings b on b.rno = r.rno, locations ls, locations ld
        where ls.lcode = r.src and ld.lcode = r.dst
        and r.rdate > datetime('now')
        group by r.driver, r.rno, r.seats, r.rdate, r.price, ls.city, ld.city;
        ''')
    # fetch the rides provided by this membber
    c.execute('''
        select rno, driver, available
        from ride_info
        where driver = ? ;
        ''', email)
    c.commit()

    ridesRows = c.fetchall()
    if len(ridesRows) > 5:
        print(ridesRows[:5])
        for i in range(5,len(ridesRows),5):
            answer = input('Enter y to see more, otherwise finish')
            if answer == 'y':
                print(ridesRows[i:i+5])
            else:
                break
    elif len(ridesRows) == 0:
        print('no ride offered found')
    else:
        print(ridesRows)

def listAllBooking(conn, c, email):
    '''
    list all bookings on rides s/he offers and cancel any booking.
    '''
    c.execute('''
        select b.rno, b.bno
        from bookings b, rides r
        where b.rno = r.rno and b.email = ? and  
        ''', email)
    c.commit()
