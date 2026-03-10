from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# URL de tu base de datos PostgreSQL
DATABASE_URL = "postgresql://libreria_pl1j_user:xkfwjqDgt5sQH4aJowvMMcdPGDnx9vYA@dpg-d6g8ojfgi27c738ruh8g-a/libreria_pl1j"

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo de la tabla
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    contenido = db.Column(db.Text)

# Crear tablas automáticamente al iniciar
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

# Ejecutar app localmente (Render usa Gunicorn)
if __name__ == "__main__":
    app.run(debug=True)