from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy

# app configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/webdevblog.db"
app.debug = False

# db configuration
db = SQLAlchemy(app)

class BlogEntry(db.Model):
  ID = db.Column(db.Integer, primary_key=True)
  author = db.Column(db.String(50))
  title = db.Column(db.String(100))
  text = db.Column(db.String(5000))
  date = db.Column(db.DateTime())

  def __init__(self, author, title, text):
    self.author = author
    self.title = title
    self.text = text
    self.date = datetime.utcnow()

  def __repr__(self):
    return "POST %s by %s on %s" %(self.title, self.author, self.date)

db.create_all()

# helper functions
def createPost(author, title, text):
  '''
  Creates a BlogEntry if given valid parameters, else return None.
  '''
  # first verify components
  if author and title and text and \
      len(author) <= 50 and len(title) <= 100 and len(text) <= 5000:
    return BlogEntry(author, title, text)
  return None

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

@app.route("/newpost", methods=["POST"])
def newpost():
  author = request.form["post-name"]
  title = request.form["post-title"]
  text = request.form["post-text"]
  post = createPost(author, title, text)
  # case invalid
  if post == None:
    return render_template("create.html")
  # success, commit to database
  else:
    db.session.add(post)
    db.session.commit()
    return redirect(url_for("home"))

# actual calls
if __name__ == "__main__":
  app.run()
