from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import bcrypt
import logging

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

username = 'root'
password = '12345'
host = 'localhost'
database = 'biblioteca'

try:
    # Create a MySQL connection
    cnx = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )
except mysql.connector.Error as err:
    app.logger.error("Error connecting to MySQL: %s", err)
    exit(1)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["user_name"]
    password = request.form["contraseña"]
    
    try:
        cursor = cnx.cursor()
        
        query = "SELECT contraseña FROM usuario WHERE user_name = %s"
        cursor.execute(query, (username,))
        
        result = cursor.fetchone()
        
        if result:
            hashed_password = result[0].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                return redirect(url_for('gestion'))
            else:
                return "Invalid password"
        else:
            return "Invalid username"
    except mysql.connector.Error as err:
        app.logger.error("Error executing query: %s", err)
        return "Error executing query"
    finally:
        cursor.close()

@app.route("/gestion")
def gestion():
    return render_template("gestion.html")

@app.route("/gestionar", methods=["POST"])
def gestionar():
    title = request.form.get("titulo")
    author = request.form.get("autor")
    genr = request.form.get("genero")
    editorial = request.form.get("editorial")
    synopsis = request.form.get("sinopsis")
    date = request.form.get("fecha_publicacion")
    status = request.form.get("estado")
    if not all([title, author, genr, editorial, synopsis, date, status]):
        app.logger.error("Error: Missing required fields")
        return "Error: Please fill in all required fields"
    try:
        cursor = cnx.cursor()
        query = "INSERT INTO libro (titulo, autor, genero, editorial, sinopsis, fecha_publicacion, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (title, author, genr, editorial, synopsis, date, status))
        cnx.commit()
        app.logger.info("Book added successfully")
        return "Libro agregado con éxito"
    except mysql.connector.Error as err:
        app.logger.error("Error executing query: %s", err)
        return "Error al agregar libro: {}".format(err)
    finally:
        cursor.close()

if __name__ == "__main__":
    app.run(debug=True)