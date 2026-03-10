from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Render puede proporcionar DATABASE_URL automáticamente
database_url = os.getenv("DATABASE_URL")

# Si no existe, usa tu conexión directa
if not database_url:
    database_url = "postgresql://libreria_pl1j_user:xkfwjqDgt5sQH4aJowvMMcdPGDnx9vYA@dpg-d6g8ojfgi27c738ruh8g-a/libreria_pl1j"

# Fix para SQLAlchemy en algunos entornos
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo de tabla
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    contenido = db.Column(db.Text)

# Crear tablas
with app.app_context():
    db.create_all()

# Página principal
@app.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)

# Agregar noticia
@app.route("/add", methods=["POST"])
def add():
    titulo = request.form["titulo"]
    contenido = request.form["contenido"]

    nuevo_post = Post(titulo=titulo, contenido=contenido)
    db.session.add(nuevo_post)
    db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run() 