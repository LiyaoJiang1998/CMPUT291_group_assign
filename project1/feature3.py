import sqlite3

def addBooking(conn, email):
    c = conn.cursor();
    # validate if the driver provided the given rno
    while True:
        rno = input('please enter the rno for the ride you want to book a member : ')
        # save the user who booked that ride:
        c.execute('''
            select driver
            from rides
            where rno = ?;
            ''',(rno,))
        driver = c.fetchone()
        if driver == None:
            print('invalid rno!!')
            choice = input('Enter y to try enter the rno again, else quit booking: ')
            if choice == 'y' or choice == 'Y':
                continue
            else:
                return
        else:
            if driver[0] == email:
                break
            else:
                print('you did not provide this ride!')
                choice = input('Enter y to try enter the rno again, else quit booking: ')
                if choice == 'y' or choice == 'Y':
                    continue
                else:
                    return

    # input member email
    while True:
        who = input('Please input who (email) you want to book for this ride: ')
        c.execute('''
            select email
            from members;
            ''')
        allEmail = [email for subtuples in c.fetchall() for email in subtuples]
        if who in allEmail:
            break
        else:
            print('this member email does not exist!')
            choice = input('Enter y to try enter the email again, else quit booking: ')
            if choice == 'y' or choice == 'Y':
                continue
            else:
                return

    # input number of seat
    while True:
        # how many seats are available?
        c.execute('''
            select available
            from ride_info
            where rno = ?;
            ''',(rno,))
        availableSeats = c.fetchone()[0]

        numSeat = input('Enter the number of seats that you want to book: ')
        try:
            numSeat = int(numSeat)
        except ValueError as e:
            print('invalid number')
            choice = input('Enter y to try enter the number again, else quit booking: ')
            if choice == 'y' or choice == 'Y':
                continue
            else:
                return

        if numSeat <= 0:
            print('invalid number')
            choice = input('Enter y to try enter the number again, else quit booking: ')
            if choice == 'y' or choice == 'Y':
                continue
            else:
                return

        elif numSeat > availableSeats:
            print('available seats are not enough, you are over booking!')
            choice = input('Enter y if you are sure, else quit booking: ')
            if choice == 'y' or choice == 'Y':
                break
            else:
                return
        else:
            break

    # input the cost per seat
    while True:
        bCost = input('Please enter the cost per seat: ')
        try:
            bCost = int(bCost)
            if bCost < 0:
                print('invalid cost')
                choice = input('Enter y to try enter the cost again, else quit booking: ')
                if choice == 'y' or choice == 'Y':
                    continue
                else:
                    return
            else:
                break

        except ValueError as e:
            print('invalid cost')
            choice = input('Enter y to try enter the cost again, else quit booking: ')
            if choice == 'y' or choice == 'Y':
                continue
            else:
                return

    # input the pickup lcode
    while True:
        plcode = input('Please enter the pickup location lcode: ')
        c.execute('''
            select lcode
            from locations;
            ''')
        allLcode = [lcode for subtuples in c.fetchall() for lcode in subtuples]
        if plcode in allLcode:
            break
        else:
            print('this lcode does not exist!')
            choice = input('Enter y to try enter the lcode again, else quit booking: ')
            if choice == 'y' or choice == 'Y':
                continue
            else:
                return

    # input the dropoff lcode
    while True:
        dlcode = input('Please eneter the dropoff location lcode: ')
        c.execute('''
            select lcode
            from locations;
            ''')
        allLcode = [lcode for subtuples in c.fetchall() for lcode in subtuples]
        if dlcode in allLcode:
            break
        else:
            print('this lcode does not exist!')
            choice = input('Enter y to try enter the lcode again, else quit booking: ')
            if choice == 'y' or choice == 'Y':
                continue
            else:
                return

    # generate a unique bno
    c.execute('''
        select max(bno)
        from bookings;
        ''')
    bno = c.fetchone()
    if bno == None:
        bno = 1
    else:
        bno = bno[0] + 1

    # now insert the information into bookings
    # bno,email,rno,cost,seats,pickup,dropoff
    c.execute('''
        insert into bookings
        values (?,?,?,?,?,?,?);
        ''',(bno,who,rno,bCost,numSeat,plcode,dlcode))
    # send the proper message
    receiver = who
    content = 'you are booked on the ride: %s, the bno is: %s'%(rno,bno)
    c.execute('''
        insert into inbox
        values (?,datetime('now','localtime'),?,?,?,?);
        ''',(receiver,email,content,rno,'n'))
    conn.commit()

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
        and r.rdate > datetime('now','localtime')
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
            answer = input('Enter y to see more, otherwise finish: ')
            if answer == 'y' or answer == 'Y':
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

    print("All the bookings associate with rides provided by you: ")
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
            where bno = ?;
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
                where b.bno = ? and b.rno = r.rno;
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

    # send massage to the user (receiver) who booked the canceled ride
    receiver = receiver[0]
    # send the proper message
    content = 'sorry, your booking bno: %s, is canceled by the driver'%(bno)
    c.execute('''
        insert into inbox
        values (?,datetime('now','localtime'),?,?,?,?);
        ''',(receiver,email,content,ridenum,'n'))

    conn.commit()

def feature3(conn, email):
    while True:
        print()
        print('Select which function to use: ')
        print('1, list all the associated bookings')
        print('2, cancel a booking')
        print('3, list all the rides you provided')
        print('4, add a booking to a ride provided by you')
        print('otherwise, go back to the main menu')
        mode = input()
        print()
        if mode == '1':
            listAllBooking(conn, email)
            print("-----------------finished-----------------")
        elif mode == '2':
            cancelBooking(conn, email)
            print("-----------------finished-----------------")
        elif mode == '3':
            listAllRides(conn, email)
            print("-----------------finished-----------------")
        elif mode == '4':
            addBooking(conn, email)
            print("-----------------finished-----------------")
        else:
            print("exiting feature3 ......")
            return

if __name__ == '__main__':
    # feature3 test
    conn = sqlite3.connect('./project1.db')
    email = 'whatever@e.com'
    feature3(conn,email)

    # email = 'joe@gmail.com' # test listAllBooking
    # listAllBooking(conn, email)
    # cancelBooking(conn, email)

    # email = 'whatever@e.com' # test listAllRides
    # listAllRides(conn, email)
    # addBooking(conn, email)
