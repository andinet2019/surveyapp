from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from sendemail import send_mail
app = Flask(__name__)
ENV = 'prod'
if ENV == 'dev':
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DB_DEV_URL')
else:
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://oyxnrhrstnyvvo:48e524e3c9279c5f7444af097bd0314abdebe55bfacffd9992dd0eac8dc0d43b@ec2-3-219-204-29.compute-1.amazonaws.com:5432/d3v7ffibrjevna"


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Survey(db.Model):
    __tablename__ = "survey"
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    realtor = db.Column(db.String(200))
    address = db.Column(db.String)
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, realtor, address, rating, comments):
        self.customer = customer
        self.realtor = realtor
        self.address = address
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    """
    index method to return index.html page
    :return:
    """
    return render_template("index.html")


@app.route('/submit', methods=["POST"])
def submit():
    """
    method to submit the form
    :return:
    """
    if request.method == "POST":
        customer = request.form["customer"]
        realtor = request.form["realtor"]
        address = request.form["address"]
        rating = request.form["rating"]
        comments = request.form["comments"]
        # validating if user has a valid input
        if customer == "" or realtor == "" or comments == "":
            return render_template('index.html', message="Please enter the required fields")
        if db.session.query(Survey).filter(Survey.customer == customer).count() == 0:
            data = Survey(customer, realtor, address, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, realtor, address, rating, comments)
            return render_template("success.html")
        return render_template("index.html",message="You have already submitted feedback")


if __name__ == "__main__":
    app.run()
