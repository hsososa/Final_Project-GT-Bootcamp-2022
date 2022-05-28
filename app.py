# import necessary libraries
from models import create_classes
import os
import jinja2
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import random
import psycopg2
from predictor import newspredictor


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://oarqmwqgvubeko:490910ef17b3f1cab937e2dcbef933411ecfad1cf7b7f994b2984a874a9b96b9@ec2-3-228-235-79.compute-1.amazonaws.com:5432/d2o9sjooi371ok"    #"sqlite:///db.sqlite"    #os.environ.get('DATABASE_URL', '') or 

#OTHER URI: "postgres://oarqmwqgvubeko:490910ef17b3f1cab937e2dcbef933411ecfad1cf7b7f994b2984a874a9b96b9@ec2-3-228-235-79.compute-1.amazonaws.com:5432/d2o9sjooi371ok"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

News = create_classes(db)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

TrueFalse=[]

TrueFalse=["True","False"]

# Query Post the form values to the database
@app.route("/send", methods=["GET","POST"])
def send():
    if request.method == "POST":
        title = request.form["articletitle"]
        text = request.form["articletext"]
        subject = request.form["articlesubject"]
        date = request.form["articledate"]
        #status = random.choice(TrueFalse)
        print(newspredictor(text))
        news = News(title=title, text=text, subject=subject, news_date=date)
        db.session.add(news)
        db.session.commit()
        return redirect("/", code=302)

    return render_template("form.html")


# Show all records that have been uploaded
@app.route('/showall')
def show_all():
   return render_template('show_all.html', News = News.query.all())    


if __name__ == "__main__":
    app.run()