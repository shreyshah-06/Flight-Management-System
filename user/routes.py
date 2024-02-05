from flask import Flask
from app import app
from user.models import User

@app.route('/user/signup',methods=['POST','GET'])

def signUp():
    return User().signUp()

@app.route('/user/signout')
def signOut():
    return User().signOut()


@app.route('/user/login',methods=['POST'])
def login():
    return User().Userlogin()

@app.route('/admin/signup',methods=['POST','GET'])
def adminsignUp():
    return User().AdminsignUp()


@app.route('/admin/login',methods=['POST'])
def adminlogin():
    return User().Adminlogin()

@app.route('/admin/addflight',methods=['POST'])
def addFlight():
    return User().addFlights();

@app.route('/getflight',methods=['POST','GET'])
def getFlight():
    return User().getFlights();

@app.route('/bookflight',methods=['POST','GET'])
def bookFlight():
    return User().bookFlight();

@app.route('/user/bookings',methods=['POST','GET'])
def userBooking():
    return User().userBooking();

@app.route('/deleteflight', methods=['DELETE'])
def deleteFlight():
    return User().deleteFlight();

@app.route('/admin_view_bookings', methods=['POST'])
def ViewBookingAdmin():
    return User().ViewBookingAdmin();