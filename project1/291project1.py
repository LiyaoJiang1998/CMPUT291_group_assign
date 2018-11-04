import sys
import sqlite3
import login
import rideRequest
import offer_a_ride
# import searchRides
import feature3
import feature4

def main():
    dbName = sys.argv[1]
    conn = sqlite3.connect('./%s'%(dbName))
    # email = login.login(conn)

    while True:
        print('''Select your operation: ''')
        op = input("1 Offer a ride.\
                    \n2 Search for rides.\
                    \n3 Book members or cancel bookings.\
                    \n4 Post ride requests.\
                    \n5 Search and delete ride requests.\
                    \n6 Logout\n")

        if op == '1':
            pass
        elif op == '2':
            pass
        elif op == '3':
            pass
        elif op == '4':
            pass
        elif op == '5':
            pass
        elif op == '6':
            pass
        else:
            print("invalid input!, please try again")
            continue

    # rides = searchRides.searchRide(conn, email)


    # while True:
    #     print('''Select your operation:''')
    #     op = input("1 Offer a ride.\n2 Search for rides.\n3 Book members or cancel bookings.\n4 Post ride requests.\n5 Search and delete ride requests.\n6 Logout")
    #
    # rideRequest.searchAndDelete(conn, email)
    # #feature3.listAllBookings(conn, email)

if __name__ == "__main__":
    main()
