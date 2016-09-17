from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy

# app configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///encrmsg.db"
app.debug = True

# db configuration
db = SQLAlchemy(app)

class BlogEntry(db.Model):
  ID = db.Column(db.Integer, primary_key=True)
  header = db.Column(db.String(50))
  # author = db.Column(db.String(30))
  text = db.Column(db.String(5000))
  date = db.Column(db.DateTime())
  question = db.Column(db.String(100))
  answer = db.Column(db.String(50))

  def __init__(self, header, text, question, answer):
    self.header = header
    self.text = text
    self.question = question
    self.answer = answer
    self.date = datetime.utcnow()

  def __repr__(self):
    return "POST %s by %s on %s" %(self.header, self.author, self.date)

class users(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "POST %s with pass %s" %(self.username, self.password)

db.create_all()

# helper functions
def createPost(header, text, question, answer):
  '''
  Creates a BlogEntry if given valid parameters, else return None.
  '''
  # first verify components
  if header and text and question and answer and \
      len(header) <= 50 and len(text) <= 5000 and len(question) <= 100 and \
      len(answer) <= 50:
    return BlogEntry(header, text, question, answer)
  return None

#def checkAnswer(question):

# routing
@app.route("/")
def home():
  # query the database for blog entries
  blogEntries = BlogEntry.query.order_by(BlogEntry.date.desc())
  return render_template("index.html", blogEntries=blogEntries)

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/create")
def create():
  return render_template("create.html")

@app.route("/profile")
def profile():
  return render_template("profile.html")

@app.route("/newpost", methods=["POST"])
def newpost():
  header = request.form["post-header"]
  text = request.form["post-text"]
  question = request.form["post-question"]
  answer = request.form["post-answer"]
  post = createPost(header, text, question, answer)
  # case invalid
  if post == None:
    return render_template("create.html")
  # success, commit to database
  else:
    db.session.add(post)
    db.session.commit()
    return redirect(url_for("home"))

#@app.route("/questionform", methods=["POST"])
#def questionform():


# actual calls
if __name__ == "__main__":
  app.run()