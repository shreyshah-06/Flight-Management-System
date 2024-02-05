from flask import Flask,jsonify,request,session,redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class User:

    def startSession(self,user):
        del user['password']
        session['loggedIn'] = True
        print(session['loggedIn'])
        session['user'] = user
        return jsonify(user),200
    def signUp(self):
        data = request.json
        user={
            "_id":uuid.uuid4().hex,
            "name":data.get('name'),
            "email":data.get('email'),
            "password":data.get('password'),
            "bookings":[]
        }
        user['password'] = pbkdf2_sha256.encrypt(user['password']);

        if db.users.find_one({"email":user['email']}):
            return jsonify({"error":"Email address alredy in use"}),400

        if db.users.insert_one(user):
            return self.startSession(user)
        return jsonify({"error":"Signup Failed"}),400
    def AdminsignUp(self):
        data = request.json
        user={
            "_id":uuid.uuid4().hex,
            "name":data.get('name'),
            "email":data.get('email'),
            "password":data.get('password'),
        }
        user['password'] = pbkdf2_sha256.encrypt(user['password']);

        if db.admindb.find_one({"email":user['email']}):
            return jsonify({"error":"Email address alredy in use"}),400

        if db.admindb.insert_one(user):
            return self.startSession(user)
        return jsonify({"error":"Signup Failed"}),400
    
    def signOut(self):
        session.clear();
        return redirect('/')
    
    def Userlogin(self):
        data = request.json
        user  = db.users.find_one({
            "email": data.get('email')
        })
        if user and pbkdf2_sha256.verify(data.get('password'), user['password']):
            return self.startSession(user)
        return jsonify({"error":"invalid credentials"}),401
    def Adminlogin(self):
        data = request.json
        user  = db.admindb.find_one({
            "email": data.get('email')
        })
        if user and pbkdf2_sha256.verify(data.get('password'), user['password']):
            return self.startSession(user)
        return jsonify({"error":"invalid credentials"}),401
    
    def addFlights(self):
        data = request.json
        if 'user' not in session or 'email' not in session['user']:
            return jsonify({"error": "User not logged in"}), 401
    
        admin_email = session['user']['email']
        flightData = {
            "adminem":admin_email,
            "flightNum":data.get('flightNum'),
            "to":data.get('to'),
            "from":data.get('from'),
            "date": data.get('date'),
            "Dtime": data.get('Dtime'),
            "ATime": data.get('ATime'),
            "price":data.get('price'),
            "seats":data.get('seats'),
            "bookingData":[]
        }
        if db.flights.find_one({"flightNum":flightData['flightNum']}):
            return jsonify({"error":"Flight already exists"}),400
        if db.flights.insert_one(flightData):
            return jsonify({"message": "Flight added successfully"}), 200
        return jsonify({"error":"Flight Adding Failed"}),400
    
    def getFlights(self):
        data = request.json
        start_date = data.get('date')
        start_time = data.get('time')
        from_city = data.get('from')
        to_city = data.get('to')
        query = {
            'date': {'$gte': start_date},
            'Dtime': {'$gte': start_time},
            'from': from_city,
            'to': to_city
        }
        search_results = db.flights.find(query)
        flights = []
        for flight in search_results:
            flights.append({
               'flightNum': flight['flightNum'],
                'to': flight['to'],
                'from': flight['from'],
                'date': flight['date'],
                'Dtime': flight['Dtime'],
                'ATime': flight['ATime'],
                'price': flight['price'],
                'seats':flight['seats']
            })

        return jsonify({'flights': flights})
    
    def bookFlight(self):
        if 'user' not in session or 'email' not in session['user']:
            return jsonify({"error": "User not logged in"}), 401
        
        data = request.json
        flight_num = data.get('flightNum')
        ticketsBook = data.get('ticketsBook')
        if ticketsBook == 0:
            return jsonify({"error": "Number of tickets cannot be zero"}), 400
        flight = db.flights.find_one({"flightNum":flight_num})
        if not flight:
            return jsonify({"error": "Flight not found"}), 404
        
        user_email = session['user']['email']
        seats_available = flight.get('seats')
        if seats_available is None:
            return jsonify({"error": "Number of available seats information is missing"}), 500
        
        if int(seats_available) < int(ticketsBook):
            return jsonify({"error": f"Not enough seats available. Available seats: {seats_available}"}), 400
        
        flight['seats'] = seats_available - ticketsBook

        bookingData = {
            "userEmail":user_email,
            "tickets":ticketsBook,
            "flightNum": flight_num
        }
        
        Userbooking_data = {
            "flightNum": flight_num,
            "seatsBooked": ticketsBook,
            "flightNum":data.get('flightNum'),
            "to":data.get('to'),
            "from":data.get('from'),
            "Atime":data.get('Atime'),
            "Dtime":data.get('Dtime'),
            "date":data.get('date')
        }

        flight.setdefault('bookingData', []).append(bookingData)
        print(flight)

        try:
        # Update the flight document in the database
            db.flights.update_one({"flightNum": flight_num}, {"$set": flight})
            db.users.update_one({"email": user_email}, {"$push": {"bookings": Userbooking_data}})
            return jsonify({"message": "Flight booked successfully"}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to book flight: {str(e)}"}), 500
        
    def userBooking(self):
        if 'user' not in session or 'email' not in session['user']:
            return jsonify({"error": "User not logged in"}), 401
    
        user_email = session['user']['email']

        try:
            user = db.users.find_one({"email": user_email})
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            user_bookings = user.get('bookings', [])
            
            return jsonify({"user_bookings": user_bookings}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to retrieve user bookings: {str(e)}"}), 500
        

    def deleteFlight(self):
        data = request.json
        flight_num = data.get('flightNum')

        flight = db.flights.find_one({"flightNum": flight_num})
        if not flight:
            return jsonify({"error": "Flight not found"}), 404

        try:
            db.flights.delete_one({"flightNum": flight_num})
            return jsonify({"message": "Flight deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to delete flight: {str(e)}"}), 500
        
    def ViewBookingAdmin(self):
        if 'user' not in session or 'email' not in session['user']:
            return jsonify({"error": "Admin not logged in"}), 401
    
        admin_email = session['user']['email']

        data = request.json
        flight_num = data.get('flightNum')
        flight_time = data.get('flightTime')

        query = {
            "$and": [
                {"$or": [
                    {"flightNum": flight_num},
                    {"Dtime": flight_time}
                ]},
                {"adminem": admin_email}
            ]
        }

        flights = db.flights.find(query)
        bookings_data = []

        for flight in flights:
            booking_data = flight.get('bookingData', [])
            bookings_data.extend(booking_data)

        return jsonify({"flight_bookings": bookings_data}), 200




        
        

