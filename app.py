from flask import Flask

app = Flask(__name__)

@app.route("/")
def bienvenida():
    return  """
        <a href="/primero">Inicio</a>
        <a href="/segundo">Medio</a>
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
    return "<a href="" "

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

