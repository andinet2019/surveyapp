from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sendemail import send_mail
# from dotenv import load_dotenv
import os

# for using secrets in .env
# load_dotenv()

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DEV_DB_URL')


else:
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ppdpdxlwrboyrk:8520b5f7656c454dcfeb96a252e55df361482f178a9ace0b5fd99bfafc727d4f@ec2-3-221-109-227.compute-1.amazonaws.com:5432/dfvp51l9598iu7"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Survey(db.Model): 
    __tablename__ = "survey_model"
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.String(200), unique=True)
    instructor = db.Column(db.String(200))
    cohort_name = db.Column(db.String)
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, student, instructor, cohort_name, rating, comments):
        self.student = student
        self.instructor = instructor
        self.cohort_name = cohort_name
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
        student = request.form["student"]
        instructor = request.form["instructor"]
        cohort_name = request.form["cohort_name"]
        rating = request.form["rating"]
        comments = request.form["comments"]

        # validating if user has a valid input
        if student == "" or instructor == "" or comments == "":
            return render_template('index.html', message="Please enter the required fields!")
        if db.session.query(Survey).filter(Survey.student == student).count() == 0:
            data = Survey(student, instructor, cohort_name, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(student, instructor, cohort_name, rating, comments)
            return render_template("success.html")
        return render_template("index.html", message="You have already submitted the feedback.Have a good day!")


if __name__ == "__main__":
    app.run()
