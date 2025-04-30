from flask import Flask, url_for
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

db = None  # Variable global para almacenar la conexión a la base de datos

# Función para abrir la conexión a la base de datos
def abrirConexion():
    global db  # Hace referencia a la variable global db
    db = sqlite3.connect("instance/datos.sqlite")  # Conecta a la base de datos SQLite
    db.row_factory = sqlite3.Row  # Configura el cursor para devolver filas como diccionarios
    return db  # Devuelve la conexión abierta

# Función para cerrar la conexión a la base de datos
def cerrarConexion():
    global db  # Hace referencia a la variable global db
    if db is not None:  # Verifica si la conexión está abierta
        db.close()  # Cierra la conexión a la base de datos
        db = None  # Establece db a None para indicar que no hay conexión activa

# Función para convertir filas de resultados de la base de datos a diccionarios
def dict_factory(cursor, row):
  """Arma un diccionario con los valores de la fila."""
  fields = [column[0] for column in cursor.description]  # Obtiene los nombres de las columnas
  return {key: value for key, value in zip(fields, row)}  # Crea un diccionario con los nombres de columna como claves y los valores de la fila como valores

# Ruta para obtener todos los usuarios de la base de datos
@app.route("/sqlite/usuario")
def obtenerGente():
    global db  # Hace referencia a la variable global db
    conexion = abrirConexion()  # Abre la conexión con la base de datos
    cursor = conexion.cursor()  # Crea un cursor para ejecutar la consulta SQL
    cursor.execute('SELECT * FROM usuarios')  # Ejecuta la consulta para seleccionar todos los usuarios
    resultado = cursor.fetchall()  # Obtiene todos los resultados de la consulta
    cerrarConexion()  # Cierra la conexión con la base de datos
    fila = [dict(row) for row in resultado]  # Convierte cada fila de resultados a diccionario
    return str(fila)  # Devuelve los resultados como una cadena de texto

# Ruta para contar cuántos registros hay en la tabla de usuarios
@app.route("/sqlite/registro")
def testRG():
   global db  # Hace referencia a la variable global db
   abrirConexion()  # Abre la conexión con la base de datos
   cursor = db.cursor()  # Crea un cursor para ejecutar la consulta SQL
   cursor.execute("SELECT COUNT(*) AS cant FROM usuarios; ")  # Ejecuta una consulta para contar los registros
   res = cursor.fetchone()  # Obtiene el primer resultado (el número de registros)
   registros = res["cant"]  # Extrae el valor del conteo
   cerrarConexion()  # Cierra la conexión con la base de datos
   return f"Hay {registros} registros en la tabla usuarios"  # Devuelve el conteo de registros

# Ruta para insertar un nuevo usuario en la base de datos
@app.route("/sqlite/<string:usuario>/<string:email>")
def testDB(usuario, email):
 conexion = abrirConexion()  # Abre la conexión con la base de datos
 cursor = conexion.cursor()  # Crea un cursor para ejecutar la consulta SQL
 # Insertamos de forma segura utilizando parámetros en lugar de concatenar valores
 db.execute("INSERT INTO usuarios (usuario, email) VALUES (?, ?)", (usuario, email))  
 conexion.commit()  # Guarda los cambios realizados en la base de datos
 # Verificamos cuántos registros hay ahora
 cursor.execute("SELECT COUNT(*) as cant FROM usuarios")  # Consulta el número de registros
 res = cursor.fetchone()  # Obtiene el resultado de la consulta
 cerrarConexion()  # Cierra la conexión con la base de datos
 registros = res["cant"]  # Extrae el número de registros
 return f"Se insertó a {usuario} con email {email}. Ahora hay {registros} registros en la tabla usuarios."  # Devuelve un mensaje de confirmación

# Ruta para actualizar un email en base al usuario en la base de datos
@app.route("/sqlite/actualizar/<string:usuario>/<string:nuevo_email>")
def testUpdate(usuario, nuevo_email):
 conexion = abrirConexion()  # Abre la conexión con la base de datos
 cursor = conexion.cursor()  # Crea un cursor para ejecutar la consulta SQL
 # Actualizmos de forma segura utilizando parámetros en lugar de concatenar valores.
 db.execute("UPDATE usuarios SET email=? WHERE usuario=?", (nuevo_email, usuario))  
 db.commit()  # Guarda los cambios realizados en la base de datos
 cerrarConexion()  # Cierra la conexión con la base de datos
 return f"Actualizamos el correo del usuario {usuario} a {nuevo_email}."  # Devuelve un mensaje de confirmación


# Ruta para borrar un usuario de la base de datos por su id
@app.route("/sqlite/delete/<int:id>")
def testDelete(id):
 # Abre la conexión con la base de datos
 conexion = abrirConexion()
 cursor = conexion.cursor()  # Crea un cursor para ejecutar la consulta SQL
 # Borramos la fila de forma segura utilizando parámetros en lugar de concatenar valores
 db.execute("DELETE FROM usuarios WHERE id=?", (id,))
 conexion.commit()  # Guarda los cambios realizados en la base de datos
 cerrarConexion()  # Cierra la conexión con la base de datos
 return f"Se borro el id {id} en la tabla usuarios."  # Devuelve un mensaje de confirmación
#by juanma
# Ruta para obtener un usuario específico de la base de datos por su id
@app.route("/sqlite/usuario/<int:id>")
def selecciónIndividual(id):
 conexion = abrirConexion()  # Abre la conexión con la base de datos
 cursor = conexion.cursor()  # Crea un cursor para ejecutar la consulta SQL
 cursor.execute('SELECT * FROM usuarios WHERE id=?', (id,))  # Ejecuta la consulta para obtener el usuario con el id dado
 resultado = cursor.fetchone()  # Obtiene el primer resultado de la consulta
 cerrarConexion()  # Cierra la conexión con la base de datos
 fila = dict(resultado)  # Convierte la fila de resultados en un diccionario
 return str(fila)  # Devuelve el resultado como una cadena de texto
