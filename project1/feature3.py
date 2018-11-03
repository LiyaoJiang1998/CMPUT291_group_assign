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

def listAllRides(conn, email):
    '''
    list all the rides the member offers with # of available seats
    '''
    c = conn.cursor();
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
        ''', (email,))
    conn.commit()

    print("All the rides provided: ")
    names = tuple(map(lambda x: x[0], c.description))
    print(names)

    ridesRows = c.fetchall()
    if len(ridesRows) > 5:
        for e in ridesRows[:5]:
            print(e)
        for i in range(5,len(ridesRows),5):
            answer = input('Enter y to see more, otherwise finish')
            if answer == 'y':
                for e in ridesRows[i:i+5]:
                    print(e)
            else:
                break
    elif len(ridesRows) == 0:
        print('no ride offered found')
    else:
        for e in ridesRows:
            print(e)

def listAllBooking(conn, email):
    '''
    list all bookings on rides s/he offers and cancel any booking.
    '''
    c = conn.cursor();

    c.execute('''
        select b.bno, b.email, b.rno, b.cost, b.seats, b.pickup, b.dropoff
        from bookings b, rides r
        where b.rno = r.rno and r.driver = ?;
        ''', (email,))
    conn.commit()

    print("All the rides provided: ")
    names = tuple(map(lambda x: x[0], c.description))
    print(names)

    bookingsRows = c.fetchall()
    for e in bookingsRows:
        print(e)

def cancelBooking(conn, email):
    c = conn.cursor();
    while True:
        bno = input('please enter the bno for the booking you need to cancel: ')
        # save the user who booked that ride:
        c.execute('''
            select email
            from bookings
            where bno = ?
            ''',(bno,))
        receiver = c.fetchone()
        if receiver == None:
            print('invalid bno!!')
            choice = input('Enter y to try enter the bno again, else quit canceling: ')
            if choice == 'y' or choice == 'Y':
                continue
            else:
                return
        else:
            c.execute('''
                select r.driver, r.rno
                from bookings b, rides r
                where b.bno = ? and b.rno = r.rno
                ''',(bno,))
            (provider,ridenum) = c.fetchone()
            if provider == email:
                break
            else:
                print('you did not provide this ride!')
                choice = input('Enter y to try enter the bno again, else quit canceling: ')
                if choice == 'y' or choice == 'Y':
                    continue
                else:
                    return

    # delete the booking row
    c.execute('''
        delete
        from bookings
        where bookings.bno = ?
        and bookings.rno in (
            select r.rno
            from rides r
            where r.driver = ?
        );
        ''',(bno,email))

    # TODO: send massage to the user (receiver) who booked the canceled ride
    receiver = receiver[0]
    # send the proper message
    content = 'sorry, your booking bno: %s, is canceled by the driver'%(bno)
    c.execute('''
        insert into inbox
        values (?,datetime('now'),?,?,?,?);
        ''',(receiver,email,content,ridenum,'n'))

    conn.commit()


if __name__ == '__main__':
    conn = sqlite3.connect('./project1.db')

    # email = 'whatever@e.com' # test listAllRides
    # listAllRides(conn, email)

    email = 'joe@gmail.com' # test listAllBooking
    listAllBooking(conn, email)
    cancelBooking(conn, email)
