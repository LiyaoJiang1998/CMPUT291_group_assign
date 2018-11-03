import sqlite3
import login
import rideRequest
#import feature3

def main():
    conn = sqlite3.connect('./pro1.db')
    email = login.login(conn)
    while True:
        print('''Select your operation:''')
        op = input("1 Offer a ride.\n2 Search for rides.\n3 Book members or cancel bookings.\n4 Post ride requests.\n5 Search and delete ride requests.\n6 Logout")

    rideRequest.searchAndDelete(conn, email)
    #feature3.listAllBookings(conn, email)

if __name__ == "__main__":
    main()
