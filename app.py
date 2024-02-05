from flask import Flask,render_template,redirect,session
from functools import wraps
from flask_cors import CORS
import pymongo
app = Flask(__name__)
CORS(app)
secretKey = b'\xab\x88\x9c\xcb\x853\xea\r\xdc>\x0eY\xb5|\xc4\xd1'
app.secret_key=secretKey
client = pymongo.MongoClient('localhost',27017)
db = client.backendtask

def loginRequired(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        if 'loggedIn' in session:
            return f(*arg,**kwargs)
    return wrap
#routes
from user import routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/dashboard')
@loginRequired
def dashboard():
    return render_template('dashboard.html')


@app.route('/admindashboard')
@loginRequired
def admindashboard():
    return render_template('dashboardAdmin.html')

@app.route('/login')
def Login():
    return render_template('login.html')
