import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# configuración base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Render usa postgres:// pero SQLAlchemy necesita postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# si no hay variable usa sqlite local
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or "sqlite:///blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo Categoría
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

# Modelo Post
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

# ruta principal
@app.route('/')
def index():
    posts = Post.query.all()
    categories = Category.query.all()
    return render_template('index.html', posts=posts, categories=categories)

# ruta para agregar post
@app.route('/post/new', methods=['GET','POST'])
def add_post():

    if request.method == 'POST':

        title = request.form['title']
        content = request.form['content']
        category_id = request.form.get('category_id')

        new_post = Post(
            title=title,
            content=content,
            category_id=category_id
        )

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('index'))

    categories = Category.query.all()

    return render_template('create_post.html', categories=categories)


# crear tablas automáticamente en el servidor
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)