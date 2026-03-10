import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Crear instancia de Flask
app = Flask(__name__)

# Configuración directa de la base de datos (tu URL)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://libreria_pl1j_user:xkfwjqDgt5sQH4aJowvMMcdPGDnx9vYA@dpg-d6g8ojfgi27c738ruh8g-a/libreria_pl1j"
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
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

# Crear tablas automáticamente
with app.app_context():
    db.create_all()

    # Crear categorías iniciales si no existen
    if Category.query.count() == 0:
        db.session.add(Category(name="Tecnología"))
        db.session.add(Category(name="Deportes"))
        db.session.add(Category(name="Política"))
        db.session.commit()

# Ruta principal
@app.route('/')
def index():
    posts = Post.query.all()
    categories = Category.query.all()
    return render_template('index.html', posts=posts, categories=categories)

# Ruta para crear un nuevo post
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

if __name__ == '__main__':
    app.run(debug=True)