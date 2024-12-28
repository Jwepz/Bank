#Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
app = Flask(__name__)

#conexion MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'bank'
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_PORT'] = 3306

conexion = MySQL(app)


@app.before_request
def before_request():
    print("antes de la peticion...")

@app.after_request
def after_request(response):
    print("despues de la peticion")
    return response

# Configuración de la clave secreta para las sesiones
app.secret_key = 'una_clave_secreta_aqui'

@app.route('/')
def landing():
     # Verifica si el usuario está autenticado en la sesión
    if 'usuario' in session:
        return f"Hola {session['usuario']}! Estás logueado."
    return '¡Hola, visitante! Por favor inicia sesión.'

    # numeros = [1,2,3,4]
    # data = {
    #     'titulo': 'index',
    #     'bienvenida': 'saludo',
    #     'numeros' : numeros,
    #     'cantidad_numeros': len(numeros)
    # }
    # return render_template('index.html', data=data)

@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
    data = {
        'titulo': 'contacto',
        'nombre': nombre,
        'edad': edad

    }
    return render_template('contacto.html', data=data)

def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return("ok")


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        correo = request.form['adress']
        password = request.form['password']
        try: 
            cursor = conexion.connection.cursor()
            sql = "SELECT adress, pass FROM users WHERE adress = %s AND pass = %s"
            cursor.execute(sql, (correo, password))
            user = cursor.fetchone()

            if(user):
                session['usuario'] = correo
                return redirect(url_for('home'))
            else:
                return "Correo o contraseña equivocado"
        except Exception as ex:
            print("Error", ex)
            return "Ocurrrio un error inesperado"
        finally:
            cursor.close()    

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Elimina el nombre de usuario de la sesión
    session.pop('usuario', None)
    return redirect(url_for('index'))

@app.route('/home')
def home():

    usuario = session['usuario']

    return render_template('home.html', data=usuario)

@app.route('/cursos')
def listar_cursos():
    data= {}
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT codigo, nombre, creditos FROM curso ORDER BY nombre ASC"
        cursor.execute(sql)
        cursos = cursor.fetchall()
       #  print(cursos)
        data['cursos'] = cursos
        data['mensaje']='Exito'
    except Exception as ex:
        data['mensaje']='Error'
    return jsonify(data)



def pagina_no_encontrada(error):
    return render_template('404.html'), 404
    #return redirect(url_for('index')) 

if __name__ == '__main__':
   app.add_url_rule('/query_string', view_func=query_string)
   app.register_error_handler(404, pagina_no_encontrada)
   app.run(debug=True, port=5000)

