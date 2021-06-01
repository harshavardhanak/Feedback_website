from enum import unique
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:9598@localhost/feedback'
else: 
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://atcimoxuuysqgy:4e38e34166bb2331774fc617a3b1456b62509cd521b45292079ec6fbecf8ac5a@ec2-52-71-231-37.compute-1.amazonaws.com:5432/daan7gforor9mt'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class feed(db.Model):
    __tablename__ = 'feedtable'
    id = db.Column(db.Integer, primary_key = True)
    customer = db.Column(db.String(200), unique = True)
    email = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text())

    def __init__(self, customer, email, dealer, rating, comment):
        self.customer = customer
        self.email = email
        self.dealer = dealer
        self.rating = rating
        self.comment = comment

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comment = request.form['comment']
        print(username, email, dealer, rating, comment)

        if username == '' or email == '' : 
            return render_template('index.html',message='Please enter the required fields.')

        if db.session.query(feed).filter(feed.customer == username).count() == 0:
                data = feed(username, email, dealer, rating, comment)
                db.session.add(data)
                db.session.commit()
                send_mail(username, dealer, rating, comment)
                return render_template('success.html')
        else:
            return render_template('index.html', message='Username is already available!')

if __name__ == '__main__' :
    app.run()
