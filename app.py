from flask import Flask, url_for, render_template #Importa render-template y la función url_for.
import sqlite3
from random import random
app = Flask(__name__)


@app.route("/")
def bienvenida():
    url_hola = url_for("inicial")
    url_segundo = url_for("saludos")
    return  f"""
        
        <a href="{url_hola}">Inicio</a>
        <div> <div>
        
        <a href="{url_segundo}">Medio</a>
        <button onclick="window.location.href='/tercero'">Final - Maluma</button>
            
            """


@app.route("/primero")
def inicial():
    return  "<h2>Y que los tragos</h2>"


@app.route("/segundo")
def saludos():
    return "<h2>hicieron estrago en su cabeza</h2>"

@app.route("/tercero")
def despedida():
    return "<a target='_blank'>HOLA</a>"

@app.route("/tercero/<string:nombre>")
def saludaremos(nombre):
    return f"<h2>No soy Maluma, soy {nombre} </h2>"

@app.route("/dado/<int:caras>")
def dado(caras):
    numero = random.randint(1, caras)
    return f"<h2>Dado con {caras} caras dio como resultado el número {numero}</h2>"

@app.route("/sumar/<int:n1>/<int:n2>")
def suma(n1, n2):
    resultado = n1 + n2
    return f"<h2>La suma entre {n1} y {n2} es {resultado}</h2>"

@app.route("/division/<int:n1>/<int:n2>")
def division(n1, n2):
    
    resultado = n1 / n2

    if n1 == 0 or n2 == 0:
        return "<h2>No se puede dividir por 0</h2>"
    else:
        return f"<h2>La división entre {n1} y {n2} da como resultado {resultado}.</h2>"




# SQLITE 

db = None  


def abrirConexion():
    global db  
    db = sqlite3.connect("instance/datos.sqlite")  # Es la conexión con la base de datos de SQLite.
    db.row_factory = sqlite3.Row  
    return db  


def cerrarConexion():
    global db  
    if db is not None:  
        db.close()  
        db = None  


def dict_factory(cursor, row):
  """Arma un diccionario con los valores de la fila."""
  fields = [column[0] for column in cursor.description]  
  return {key: value for key, value in zip(fields, row)}  


@app.route("/sqlite/usuario")
def obtenerGente():
    global db  
    conexion = abrirConexion()  
    cursor = conexion.cursor()  
    cursor.execute('SELECT * FROM usuarios')  
    resultado = cursor.fetchall()  
    cerrarConexion()  
    fila = [dict(row) for row in resultado]  # Convierte cada fila en un diccionario
    return str(fila)  


@app.route("/sqlite/registro")
def testRG():
   global db  
   abrirConexion()  
   db = db.cursor()  
   db.execute("SELECT COUNT(*) AS cant FROM usuarios; ")  
   res = db.fetchone()  
   registros = res["cant"]  
   cerrarConexion()  
   return f"Hay {registros} registros en la tabla usuarios"  # Indica la cantidad de registros


@app.route("/sqlite/<string:usuario>/<string:email>")
def testDB(usuario, email):
 conexion = abrirConexion()  
 db = conexion.cursor()  
 
 db.execute("INSERT INTO usuarios (usuario, email) VALUES (?, ?)", (usuario, email))  
 conexion.commit()  
 
 db.execute("SELECT COUNT(*) as cant FROM usuarios")  
 res = db.fetchone()  
 cerrarConexion()  # Cierra la conexión con la base de datos
 registros = res["cant"]  
 return f"Se insertó a {usuario} con email {email}. Ahora hay {registros} registros en la tabla usuarios."  # Devuelve un mensaje de confirmación


@app.route("/sqlite/actualizar/<string:usuario>/<string:nuevo_email>")
def testUpdate(usuario, nuevo_email):
 conexion = abrirConexion()  
 db = conexion.cursor()  

 db.execute("UPDATE usuarios SET email=? WHERE usuario=?", (nuevo_email, usuario))  
 db.commit()  
 cerrarConexion() 
 return f"Actualizamos el correo del usuario {usuario} a {nuevo_email}." 

# Ruta para borrar un usuario de la base de datos por su id
@app.route("/sqlite/delete/<int:id>")
def testDelete(id):
 conexion = abrirConexion()
 db = conexion.cursor() 
 db.execute("DELETE FROM usuarios WHERE id=?", (id,))
 db.commit()  
 cerrarConexion()  
 return f"Se borro el id {id} en la tabla usuarios."  

# Ruta para obtener un usuario específico de la base de datos por su id
@app.route("/sqlite/usuario/<int:id>")
def selecciónIndividual(id):
 conexion = abrirConexion()  
 db = conexion.cursor()  
 db.execute('SELECT * FROM usuarios WHERE id=?', (id,))  
 resultado = db.fetchone()  # Extrae el primer resultado de la consulta anterior.
 cerrarConexion()  
 fila = dict(resultado)  
 return str(fila)  # Retorna el resultado como un string.

# Ruta con Template

@app.route('/sqlite/mostrar-datos/<int:id>')
def datos_sqlite(id):
   abrirConexion()
   cursor = db.cursor()
   cursor.execute('SELECT id, usuario, email FROM usuarios WHERE id = ?; ', ((id,)))
   res = cursor.fetchone()
   cerrarConexion()
   usuario = None
   email = None
   if res != None:
      usuario = res['usuario']
      email = res['email']
      return render_template("template1.html", id=id, usuario=usuario, email=email)


