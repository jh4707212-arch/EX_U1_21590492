import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# usar la variable de entorno de Render
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELO CATEGORY
class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

# MODELO POST
class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship("Category", backref=db.backref("posts", lazy=True))

# CREAR TABLAS AUTOMÁTICAMENTE
with app.app_context():
    db.create_all()

# RUTA PRINCIPAL
@app.route("/")
def index():
    posts = Post.query.all()
    categories = Category.query.all()
    return render_template("index.html", posts=posts, categories=categories)

# CREAR POST
@app.route("/post/new", methods=["GET","POST"])
def add_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        category_id = request.form.get("category_id")

        post = Post(
            title=title,
            content=content,
            category_id=category_id
        )

        db.session.add(post)
        db.session.commit()

        return redirect(url_for("index"))

    categories = Category.query.all()
    return render_template("create_post.html", categories=categories)

if __name__ == "__main__":
    app.run(debug=True)