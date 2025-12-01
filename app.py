from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_from_directory
import mysql.connector
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import json   



app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

# =========================
# Conexión a la base de datos
# =========================
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='edu_cursos'
    )

# ==========================
# 🔒 Evitar cache del navegador
# ==========================
@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# ==========================
# 🔐 LOGIN ADMIN
# ==========================
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('Campus/index.html')

    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM usuarios WHERE email=%s AND password=%s AND rol='admin'",
        (email, password)
    )
    admin = cursor.fetchone()
    cursor.close()
    conn.close()

    if admin:
        session['admin_id'] = admin['id_usuario']
        session['admin_nombre'] = admin['nombre']
        session['es_admin'] = True
        return redirect(url_for('admin_panel'))
    else:
        return render_template('Campus/index.html', error="Credenciales incorrectas o no eres admin")


@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))



# ==========================
# Ruta para el campus (inicio)
# ==========================

@app.route('/bienvenida_campus')
def inicio():
    return render_template('Campus/index.html')

@app.route('/logout')
def logout():
    session.clear()  # borra todos los datos de sesión
    return redirect(url_for('inicio'))  # apunta al endpoint 'inicio'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Primero chequeamos en la tabla de usuarios normales
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM usuarios WHERE email=%s AND password=%s",
            (email, password)
        )
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        # ---------------------------
        # Si coincide con un usuario normal
        if usuario:
            session['usuario_id'] = usuario.get('id_usuario')
            session['nombre'] = usuario.get('nombre')
            session['apellido'] = usuario.get('apellido')
            session['email'] = usuario.get('email')
            session['fecha_nacimiento'] = usuario.get('fecha_nacimiento')
            session['dni'] = usuario.get('dni')
            session['telefono'] = usuario.get('telefono')

            # 🔹 Si el usuario es admin (rol en DB)
            if usuario.get('rol') == 'admin':
                session['es_admin'] = True
                return redirect(url_for('admin_panel'))

            return redirect(url_for('mis_cursos'))

        # ---------------------------
        # Si coincide con el admin “fijo” (por si no está en DB)
        if email == 'admin@educacionit.com' and password == 'admin123':
            session['es_admin'] = True
            return redirect(url_for('admin_panel'))

        # Si nada coincide
        return "Usuario o contraseña incorrectos", 403

    # Si es GET, simplemente renderizamos el formulario de login
    return render_template('Campus/index.html')




@app.route('/campus')
def inicio_campus():
    if 'usuario_id' not in session and 'es_admin' not in session:
        # Si no hay sesión, redirige al login
        return redirect(url_for('inicio'))
    return render_template('Campus/inicio_campus.html')

@app.route('/mis_cursos')
def mis_cursos():
    usuario_id = session.get('usuario_id')
    print("Usuario en sesión:", usuario_id)  # <-- Aquí se prueba
    if not usuario_id:
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.id_curso, c.titulo, c.descripcion, c.imagen
        FROM cursos c
        INNER JOIN inscripciones i ON c.id_curso = i.id_curso
        WHERE i.id_usuario = %s
        ORDER BY i.fecha_inscripcion DESC
    """, (usuario_id,))
    cursos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('Campus/mis_cursos.html', cursos=cursos)


## ===================================
## CURSO .NET (MODIFICADO)
## ===================================

@app.route('/curso/net')
def curso_net():
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return redirect(url_for('inicio'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (usuario_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('Campus/Cursos/dotnet/campus.html', usuario=usuario)


@app.route('/curso/net/prueba')
def curso_net_prueba():
    return render_template('Campus/Cursos/dotnet/prueba.html')

@app.route('/curso/net/certificado')
def curso_net_certificado():
    return render_template('Campus/Cursos/dotnet/certificado.html')

## ===================================
## CURSO JAVA
## ===================================

@app.route('/curso/java')
def curso_java():
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return redirect(url_for('inicio'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (usuario_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('Campus/Cursos/Java/campus.html', usuario=usuario)


@app.route('/curso/java/prueba')
def curso_java_prueba():
    return render_template('Campus/Cursos/Java/prueba.html')

@app.route('/curso/java/certificado')
def curso_java_certificado():
    return render_template('Campus/Cursos/Java/certificado.html')

## ===================================
## CURSO JAVASCRIPT
## ===================================

@app.route('/curso/javascript')
def curso_javascript():
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return redirect(url_for('inicio'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (usuario_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('Campus/Cursos/Javascript/campus.html', usuario=usuario)


@app.route('/curso/javascript/prueba')
def curso_javascript_prueba():
    return render_template('Campus/Cursos/Javascript/prueba.html')

@app.route('/curso/javascript/certificado')
def curso_javascript_certificado():
    return render_template('Campus/Cursos/Javascript/certificado.html')


## ===================================
## CURSO PYTHON
## ===================================

@app.route('/curso/python')
def curso_python():
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return redirect(url_for('inicio'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (usuario_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('Campus/Cursos/Python/campus.html', usuario=usuario)


@app.route('/curso/python/prueba')
def curso_python_prueba():
    return render_template('Campus/Cursos/Python/prueba.html')

@app.route('/curso/python/certificado')
def curso_python_certificado():
    return render_template('Campus/Cursos/Python/certificado.html')


## ===================================
## CURSO MANEJO IA (MODIFICADO)
## ===================================

@app.route('/curso/manejoia')
def curso_manejoia():
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return redirect(url_for('inicio'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (usuario_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('Campus/Cursos/ManejoIA/campus.html', usuario=usuario)

@app.route('/curso/manejoia/prueba')
def curso_manejoia_prueba():
    return render_template('Campus/Cursos/ManejoIA/prueba.html')


@app.route('/curso/manejoia/certificado')
def curso_manejoia_certificado():
    return render_template('Campus/Cursos/ManejoIA/certificado.html')


## ===================================
## CURSO CHAT GPT
## ===================================

@app.route('/curso/chatgpt')
def curso_chatgpt():
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return redirect(url_for('inicio'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (usuario_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('Campus/Cursos/ChatGPT/campus.html', usuario=usuario)

@app.route('/curso/chatgpt/prueba')
def curso_chatgpt_prueba():
    return render_template('Campus/Cursos/ChatGPT/prueba.html')


@app.route('/curso/chatgpt/certificado')
def curso_chatgpt_certificado():
    return render_template('Campus/Cursos/ChatGPT/certificado.html')


## ===================================
## CURSO IA PARA CONTENIDO VISUAL
## ===================================

@app.route('/curso/iaparacontenidos')
def curso_iaparacontenidos():
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return redirect(url_for('inicio'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (usuario_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('Campus/Cursos/IAparaContenidos/campus.html', usuario=usuario)

@app.route('/curso/iaparacontenidos/prueba')
def curso_iaparacontenidos_prueba():
    return render_template('Campus/Cursos/IAparaContenidos/prueba.html')


@app.route('/curso/IAparaContenidos/certificado')
def curso_iaparacontenidos_certificado():
    return render_template('Campus/Cursos/IAparaContenidos/certificado.html')

## ===================================
## CURSO IA PARA PROYECTOS
## ===================================

@app.route('/curso/iaparaproyectos')
def curso_iaparaproyectos():
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return redirect(url_for('inicio'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (usuario_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('Campus/Cursos/IAparaProyectos/campus.html', usuario=usuario)

@app.route('/curso/iaparaproyectos/prueba')
def curso_iaparaproyectos_prueba():
    return render_template('Campus/Cursos/IAparaProyectos/prueba.html')


@app.route('/curso/IAparaProyectos/certificado')
def curso_iaparaproyectos_certificado():
    return render_template('Campus/Cursos/IAparaProyectos/certificado.html')



@app.route('/inscribirse/<int:curso_id>', methods=['POST'])
def inscribirse(curso_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM inscripciones
        WHERE id_usuario = %s AND id_curso = %s
    """, (usuario_id, curso_id))

    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO inscripciones (id_usuario, id_curso)
            VALUES (%s, %s)
        """, (usuario_id, curso_id))
        conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('mis_cursos'))





# =========================
# Rutas Educacionit
# =========================
@app.route('/')
def index():
    return render_template('Educacionit/index.html')

@app.route('/cursos')
def cursos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cursos ORDER BY categoria, id_curso")
    cursos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Pasamos los cursos a la plantilla
    return render_template('Educacionit/cursos.html', cursos=cursos)


@app.route('/pago_cursos')
def pago_cursos():
    return render_template('Educacionit/pago_cursos.html')

@app.route('/seleccion_cursos/<int:curso_id>')
def seleccion_cursos(curso_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cursos WHERE id_curso = %s", (curso_id,))
    curso = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('Educacionit/seleccion_cursos.html', curso=curso)

# ========================================
# 🆕 RUTAS PARA COMPRA RÁPIDA (USUARIOS EXISTENTES)
# ========================================

@app.route('/compra-rapida/<int:curso_id>')
def compra_rapida(curso_id):
    """Muestra el formulario reducido para usuarios registrados"""
    # Guardar el curso en la sesión
    session['curso_id_temporal'] = curso_id
    
    # Obtener info del curso para mostrarlo
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cursos WHERE id_curso = %s", (curso_id,))
    curso = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('Educacionit/compra_rapida.html', curso=curso)


@app.route('/validar-usuario', methods=['POST'])
def validar_usuario_existente():
    """Valida si el usuario existe en la base de datos con email y contraseña"""
    
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    
    # Validación básica
    if not email or not password:
        flash('Por favor completá todos los campos', 'error')
        curso_id = session.get('curso_id_temporal')
        return redirect(url_for('compra_rapida', curso_id=curso_id))
    
    # Buscar usuario en la base de datos
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Consulta SQL
        query = """
            SELECT id_usuario, nombre, apellido, email, dni, telefono, fecha_nacimiento
            FROM usuarios
            WHERE email = %s AND password = %s
        """
        
        cursor.execute(query, (email, password))
        usuario = cursor.fetchone()
        
        if usuario:
            # Usuario encontrado — Guardamos datos en sesión
            session['usuario_existente'] = {
                'id': usuario['id_usuario'],
                'nombre': usuario['nombre'],
                'apellido': usuario['apellido'],
                'email': usuario['email'],
                'dni': usuario['dni'],
                'telefono': usuario['telefono'],
                'fecha_nacimiento': str(usuario['fecha_nacimiento']) if usuario['fecha_nacimiento'] else None
            }

            session['usuario_id'] = usuario['id_usuario']
            session['nombre'] = usuario['nombre']
            session['apellido'] = usuario['apellido']
            session['email'] = usuario['email']
            session['dni'] = usuario['dni']
            session['telefono'] = usuario['telefono']
            session['fecha_nacimiento'] = str(usuario['fecha_nacimiento']) if usuario['fecha_nacimiento'] else None

            curso_id = session.get('curso_id_temporal')

            if curso_id:
                flash(f'¡Bienvenido de nuevo, {usuario["nombre"]}! Continuá con tu pago.', 'success')
                return redirect(url_for('pago', id_curso=curso_id))

            else:
                flash(f'¡Bienvenido de nuevo, {usuario["nombre"]}!', 'success')
                return redirect(url_for('cursos'))
        
        else:
            flash('Email o contraseña incorrectos. Si no tenés cuenta, usá el formulario completo.', 'error')
            curso_id = session.get('curso_id_temporal')
            return redirect(url_for('compra_rapida', curso_id=curso_id))
    
    except Exception as e:
        print(f"Error en la consulta: {e}")
        flash('Ocurrió un error al verificar tus datos', 'error')
        curso_id = session.get('curso_id_temporal')
        return redirect(url_for('compra_rapida', curso_id=curso_id))
    
    finally:
        cursor.close()
        conn.close()


# =========================
# Registrar usuario (y redirigir al pago)
# =========================
@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    email = request.form.get('email')
    password = request.form.get('password')
    fecha_nacimiento = request.form.get('fecha_nacimiento') or None
    dni = request.form.get('dni') or None
    telefono = request.form.get('telefono') or None
    id_curso = request.form.get('id_curso')  # puede ser None si no viene

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Insertar nuevo usuario (agregué los campos fecha_nacimiento, dni y telefono)
    cursor.execute("""
        INSERT INTO usuarios (nombre, apellido, email, password, fecha_nacimiento, dni, telefono)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (nombre, apellido, email, password, fecha_nacimiento, dni, telefono))
    conn.commit()

    # Obtener id del usuario creado
    id_usuario = cursor.lastrowid

    # Leer usuario desde la BD (opcional, pero así te aseguras de tener todos los campos)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    # Guardar datos relevantes en session para que la página de pago los muestre
    session['usuario_id'] = id_usuario
    if usuario:
        session['nombre'] = usuario.get('nombre')
        session['apellido'] = usuario.get('apellido')
        session['email'] = usuario.get('email')
        session['fecha_nacimiento'] = usuario.get('fecha_nacimiento')
        session['dni'] = usuario.get('dni')
        session['telefono'] = usuario.get('telefono')

    # Redirigir al pago del curso elegido (si id_curso existe)
    if id_curso:
        try:
            id_curso_int = int(id_curso)
        except:
            id_curso_int = None
        if id_curso_int:
            return redirect(url_for('pago', id_curso=id_curso_int))

    # Si no se pasó curso, redirigir a la lista de cursos
    return redirect(url_for('cursos'))



# =========================
# Mostrar la página de pago (ahora recibe usuario desde sesión ó DB)
# =========================
@app.route('/pago/<int:id_curso>')
def pago(id_curso):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cursos WHERE id_curso = %s", (id_curso,))
    curso = cursor.fetchone()
    cursor.close()
    conn.close()

    if not curso:
        return "Curso no encontrado", 404

    # Intentar obtener usuario desde session — si existe, consultar BD para asegurar datos
    usuario = None
    usuario_id = session.get('usuario_id')
    if usuario_id:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (usuario_id,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        # también podríamos usar los valores en session si preferís

    # Pasamos 'curso' y 'usuario' al template
    return render_template('Educacionit/pago_cursos.html', curso=curso, usuario=usuario)



# ==========================================
# Ruta que guarda el pago e inscribe al usuario
# ==========================================
@app.route('/confirmar_pago', methods=['POST'])
def confirmar_pago():
    data = request.get_json()
    print("📦 Datos recibidos:", data)  # Para depuración

    try:
        # ✅ Usamos el usuario que está logueado en la sesión
        id_usuario = session.get('usuario_id')
        if not id_usuario:
            return jsonify({'error': 'No hay usuario logueado'}), 403

        # ✅ Tomamos el curso y el resto de los datos desde el JSON
        id_curso = int(data.get('id_curso'))
        monto = float(data.get('monto'))
        metodo_pago = data.get('metodo_pago')
        estado_pago = data.get('estado_pago', 'Aprobado')

        if not all([id_curso, monto, metodo_pago]):
            return jsonify({'error': 'Faltan datos'}), 400

        # 1️⃣ Conexión a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()

        # 2️⃣ Registrar el pago
        sql_pago = """
            INSERT INTO pagos (id_usuario, id_curso, monto, metodo_pago, fecha_pago, estado_pago)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores_pago = (id_usuario, id_curso, monto, metodo_pago, datetime.now(), estado_pago)
        cursor.execute(sql_pago, valores_pago)

        # 3️⃣ Si el pago fue aprobado, crear inscripción
        if estado_pago == "Aprobado":
            sql_inscripcion = """
                INSERT INTO inscripciones (id_usuario, id_curso, fecha_inscripcion, estado)
                VALUES (%s, %s, %s, %s)
            """
            valores_inscripcion = (id_usuario, id_curso, datetime.now(), "Inscripto")
            cursor.execute(sql_inscripcion, valores_inscripcion)

        conn.commit()
        cursor.close()
        conn.close()

        # 4️⃣ Enviar respuesta con redirección al campus o mis cursos
        return jsonify({
            'mensaje': '✅ Pago registrado e inscripción creada con éxito',
            'redirect': url_for('mis_cursos')
        }), 200

    except Exception as e:
        print("❌ Error al registrar el pago:", e)
        return jsonify({'error': str(e)}), 500


@app.route('/nosotros')
def nosotros():
    return render_template('Educacionit/nosotros.html')

@app.route('/profesores')
def profesores():
    return render_template('Educacionit/profesores.html')

@app.route('/contacto')
def contacto():
    return render_template('Educacionit/contacto.html')

# ================================================
# RUTAS DE PROGRESO
# ================================================
@app.route('/api/progreso/<int:id_curso>', methods=['GET'])
def obtener_progreso(id_curso):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'error': 'Usuario no autenticado'}), 401
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM progreso 
            WHERE id_usuario = %s AND id_curso = %s
        """, (usuario_id, id_curso))
        progreso = cursor.fetchone()
        cursor.close()
        conn.close()

        if progreso:
            return jsonify({
                'existe': True,
                'modulo_actual': progreso['modulo_actual'],
                'tema_actual': progreso['tema_actual'],
                'datos_progreso': json.loads(progreso['datos_progreso']) if progreso['datos_progreso'] else None,
                'curso_completado': bool(progreso['curso_completado'])
            }), 200
        else:
            return jsonify({'existe': False, 'mensaje': 'No hay progreso guardado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/progreso/<int:id_curso>', methods=['POST'])
def guardar_progreso(id_curso):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'error': 'Usuario no autenticado'}), 401
    
    try:
        data = request.get_json()
        modulo_actual = data.get('modulo_actual', 0)
        tema_actual = data.get('tema_actual', 0)
        datos_progreso = data.get('datos_progreso')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT curso_completado FROM progreso 
            WHERE id_usuario = %s AND id_curso = %s
        """, (usuario_id, id_curso))
        
        registro_existente = cursor.fetchone()
        
        if registro_existente and registro_existente['curso_completado'] == 1:
            curso_completado_final = 1
        else:
            curso_completado_final = 0

        datos_json = json.dumps(datos_progreso) if datos_progreso else None

        cursor.execute("""
            INSERT INTO progreso (id_usuario, id_curso, modulo_actual, tema_actual, datos_progreso, curso_completado)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                modulo_actual = VALUES(modulo_actual),
                tema_actual = VALUES(tema_actual),
                datos_progreso = VALUES(datos_progreso),
                curso_completado = GREATEST(curso_completado, VALUES(curso_completado)),
                fecha_ultima_actualizacion = CURRENT_TIMESTAMP
        """, (usuario_id, id_curso, modulo_actual, tema_actual, datos_json, curso_completado_final))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'mensaje': 'Progreso guardado exitosamente',
            'guardado': True,
            'curso_completado': curso_completado_final
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/progreso/<int:id_curso>/completar', methods=['POST'])
def completar_curso(id_curso):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'error': 'Usuario no autenticado'}), 401
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE progreso 
            SET curso_completado = 1, fecha_ultima_actualizacion = CURRENT_TIMESTAMP
            WHERE id_usuario = %s AND id_curso = %s
        """, (usuario_id, id_curso))
        conn.commit()

        if cursor.rowcount > 0:
            cursor.close()
            conn.close()
            return jsonify({'mensaje': 'Curso completado exitosamente', 'completado': True}), 200
        else:
            cursor.execute("""
                INSERT INTO progreso (id_usuario, id_curso, modulo_actual, tema_actual, curso_completado)
                VALUES (%s, %s, 0, 0, 1)
            """, (usuario_id, id_curso))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'mensaje': 'Curso completado exitosamente', 'completado': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/progreso/<int:id_curso>/reiniciar', methods=['DELETE'])
def reiniciar_progreso(id_curso):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'error': 'Usuario no autenticado'}), 401
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM progreso WHERE id_usuario = %s AND id_curso = %s", (usuario_id, id_curso))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensaje': 'Progreso reiniciado exitosamente', 'reiniciado': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# CERTIFICADO
@app.route('/api/curso/<int:id_curso>/nota', methods=['POST'])
def registrar_nota_final(id_curso):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'error': 'Usuario no autenticado'}), 401

    data = request.get_json()
    nota = float(data.get('nota', 0))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        UPDATE progreso
        SET nota_final = %s, fecha_ultima_actualizacion = CURRENT_TIMESTAMP
        WHERE id_usuario = %s AND id_curso = %s
    """, (nota, usuario_id, id_curso))
    conn.commit()

    if nota >= 7:
        cursor.execute("""
            UPDATE inscripciones SET estado = 'Finalizado'
            WHERE id_usuario = %s AND id_curso = %s
        """, (usuario_id, id_curso))
        conn.commit()

        cursor.execute("""
            SELECT i.id_inscripcion, u.nombre, u.apellido, c.titulo
            FROM inscripciones i
            JOIN usuarios u ON i.id_usuario = u.id_usuario
            JOIN cursos c ON i.id_curso = c.id_curso
            WHERE i.id_usuario = %s AND i.id_curso = %s
        """, (usuario_id, id_curso))
        info = cursor.fetchone()

        cursor.execute("SELECT id_certificado FROM certificados WHERE id_inscripcion = %s", (info['id_inscripcion'],))
        cert = cursor.fetchone()

        if not cert:
            import uuid, os, requests
            from datetime import date

            codigo_unico = str(uuid.uuid4())[:8].upper()
            cursor.execute("INSERT INTO certificados (id_inscripcion, codigo_unico) VALUES (%s, %s)", (info['id_inscripcion'], codigo_unico))
            conn.commit()
            id_certificado = cursor.lastrowid

            plantilla = "static/certificado_base.png"
            imagen = Image.open(plantilla).convert("RGBA")

            fuente_url = "https://gitlab.pg.innopolis.university/sdr-sum24/elect-gen-core/-/raw/6079817485494ab5857cf27e73ed22a53160954c/fonts/Montserrat-Bold.ttf"
            fuente_path = "static/Montserrat-Bold.ttf"
            if not os.path.exists(fuente_path):
                r = requests.get(fuente_url)
                with open(fuente_path, "wb") as f:
                    f.write(r.content)

            draw = ImageDraw.Draw(imagen)
            fuente_nombre = ImageFont.truetype(fuente_path, 90)
            fuente_curso = ImageFont.truetype(fuente_path, 70)
            fuente_fecha = ImageFont.truetype(fuente_path, 36)

            nombre_completo = f"{info['nombre']} {info['apellido']}"
            fecha_emision = date.today().strftime("%d/%m/%Y")

            bbox = fuente_nombre.getbbox(nombre_completo)
            x = (imagen.width - (bbox[2] - bbox[0])) / 2
            draw.text((x, 600), nombre_completo, fill="black", font=fuente_nombre)

            bbox2 = fuente_curso.getbbox(info['titulo'])
            x2 = (imagen.width - (bbox2[2] - bbox2[0])) / 2
            draw.text((x2, 720), info['titulo'], fill="black", font=fuente_curso)

            draw.text((1130, 920), fecha_emision, fill="black", font=fuente_fecha)
            draw.text((100, 980), f"Código: {codigo_unico}", fill="gray", font=fuente_fecha)

            os.makedirs("static/certificados", exist_ok=True)
            filename = f"certificado_{id_certificado}.png"
            filepath = os.path.join("static/certificados", filename)
            imagen.convert("RGB").save(filepath, "PNG", quality=95)

            cursor.execute("UPDATE certificados SET url_pdf = %s WHERE id_certificado = %s", (filepath, id_certificado))
            conn.commit()

        cursor.close()
        conn.close()
        return jsonify({'mensaje': '✅ Aprobado y certificado generado', 'aprobado': True}), 200

    cursor.close()
    conn.close()
    return jsonify({'mensaje': '❌ Nota registrada, pero no aprobó', 'aprobado': False}), 200


@app.route('/api/mis_certificados')
def mis_certificados():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'error': 'Usuario no autenticado'}), 401

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.id_certificado, c.url_pdf, c.codigo_unico, cur.titulo AS curso
        FROM certificados c
        JOIN inscripciones i ON c.id_inscripcion = i.id_inscripcion
        JOIN cursos cur ON i.id_curso = cur.id_curso
        WHERE i.id_usuario = %s
        ORDER BY c.fecha_emision DESC
    """, (usuario_id,))
    certificados = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'certificados': certificados})

# =====================================================
# REEMBOLSOS
# =====================================================
@app.route('/api/reembolsos', methods=['POST'])
def crear_reembolso():
    try:
        data = request.get_json()
        id_curso = data.get('id_pago')
        motivo = data.get('motivo')
        email_usuario = data.get('email_usuario')

        if not id_curso or not motivo or not email_usuario:
            return jsonify({'error': 'Faltan campos requeridos'}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s", (email_usuario,))
        usuario = cursor.fetchone()

        if not usuario:
            cursor.close()
            conn.close()
            return jsonify({'error': 'No se encontró el usuario'}), 404

        id_usuario = usuario['id_usuario']

        cursor.execute("""
            SELECT id_pago FROM pagos 
            WHERE id_curso = %s AND id_usuario = %s AND estado_pago = 'Aprobado'
            ORDER BY fecha_pago DESC LIMIT 1
        """, (id_curso, id_usuario))
        pago = cursor.fetchone()

        if not pago:
            cursor.close()
            conn.close()
            return jsonify({'error': 'No se encontró un pago aprobado'}), 404

        id_pago = pago['id_pago']

        cursor.execute("INSERT INTO reembolsos (id_pago, motivo) VALUES (%s, %s)", (id_pago, motivo))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensaje': 'Solicitud registrada correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reembolsos', methods=['GET'])
def listar_reembolsos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.id_reembolso, r.motivo, r.estado_reembolso,
                   u.nombre AS nombre_usuario, u.apellido AS apellido_usuario,
                   c.titulo AS curso
            FROM reembolsos r
            JOIN pagos p ON r.id_pago = p.id_pago
            JOIN usuarios u ON p.id_usuario = u.id_usuario
            JOIN cursos c ON p.id_curso = c.id_curso
            ORDER BY r.fecha_solicitud DESC
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ======================
# PANEL ADMIN
# ======================
@app.route('/admin')
def admin_panel():
    if not session.get('es_admin'):
        return redirect(url_for('admin_login'))
    return render_template('Educacionit/admin_panel.html')

@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario, nombre, apellido, email, rol FROM usuarios ORDER BY id_usuario")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/progreso_admin', methods=['GET'])
def listar_progreso():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT pr.id_progreso, pr.id_usuario,
                   u.nombre AS nombre, u.apellido AS apellido,
                   c.titulo AS curso,
                   CONCAT(pr.modulo_actual, '/', pr.tema_actual) AS avance,
                   IF(pr.curso_completado = 1, '100%', CONCAT(ROUND((pr.modulo_actual / 10) * 100), '%')) AS porcentaje
            FROM progreso pr
            JOIN usuarios u ON pr.id_usuario = u.id_usuario
            JOIN cursos c ON pr.id_curso = c.id_curso
            ORDER BY pr.fecha_ultima_actualizacion DESC
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pagos', methods=['GET'])
def listar_pagos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id_pago, 
                   u.nombre AS nombre_usuario, u.apellido AS apellido_usuario,
                   c.titulo AS curso,
                   p.monto, p.metodo_pago, p.estado_pago,
                   DATE_FORMAT(p.fecha_pago, '%d/%m/%Y') AS fecha
            FROM pagos p
            JOIN usuarios u ON p.id_usuario = u.id_usuario
            JOIN cursos c ON p.id_curso = c.id_curso
            ORDER BY p.fecha_pago DESC
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================================================
#  RUTAS CRUD 
# =====================================================

# ELIMINAR USUARIO (con validación de cursos activos)
@app.route('/api/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    if not session.get('es_admin'):
        return jsonify({'error': 'No autorizado'}), 403
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # ✅ Verificar si tiene cursos activos (inscripciones)
        cursor.execute("""
            SELECT COUNT(*) as total 
            FROM inscripciones 
            WHERE id_usuario = %s AND estado = 'Inscripto'
        """, (id_usuario,))
        resultado = cursor.fetchone()
        
        if resultado['total'] > 0:
            cursor.close()
            conn.close()
            return jsonify({
                'error': 'No se puede eliminar. El usuario tiene cursos activos.',
                'cursos_activos': resultado['total']
            }), 400
        
        # ✅ Si no tiene cursos activos, eliminar
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensaje': 'Usuario eliminado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# EDITAR USUARIO
@app.route('/api/usuarios/<int:id_usuario>', methods=['PUT'])
def editar_usuario(id_usuario):
    if not session.get('es_admin'):
        return jsonify({'error': 'No autorizado'}), 403
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuarios 
            SET nombre=%s, apellido=%s, email=%s, rol=%s
            WHERE id_usuario=%s
        """, (data['nombre'], data['apellido'], data['email'], data['rol'], id_usuario))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensaje': 'Usuario actualizado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ PROGRESO ============

# EDITAR PROGRESO
@app.route('/api/progreso_admin/<int:id_progreso>', methods=['PUT'])
def editar_progreso_admin(id_progreso):
    if not session.get('es_admin'):
        return jsonify({'error': 'No autorizado'}), 403
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE progreso 
            SET modulo_actual=%s, tema_actual=%s, curso_completado=%s
            WHERE id_progreso=%s
        """, (data['modulo_actual'], data['tema_actual'], data['curso_completado'], id_progreso))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensaje': 'Progreso actualizado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ELIMINAR PROGRESO
@app.route('/api/progreso_admin/<int:id_progreso>', methods=['DELETE'])
def eliminar_progreso(id_progreso):
    if not session.get('es_admin'):
        return jsonify({'error': 'No autorizado'}), 403
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM progreso WHERE id_progreso = %s", (id_progreso,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensaje': 'Progreso eliminado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ PAGOS ============

# EDITAR PAGO
@app.route('/api/pagos/<int:id_pago>', methods=['PUT'])
def editar_pago(id_pago):
    if not session.get('es_admin'):
        return jsonify({'error': 'No autorizado'}), 403
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pagos 
            SET monto=%s, metodo_pago=%s, estado_pago=%s
            WHERE id_pago=%s
        """, (data['monto'], data['metodo_pago'], data['estado_pago'], id_pago))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensaje': 'Pago actualizado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ELIMINAR PAGO
@app.route('/api/pagos/<int:id_pago>', methods=['DELETE'])
def eliminar_pago(id_pago):
    if not session.get('es_admin'):
        return jsonify({'error': 'No autorizado'}), 403
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pagos WHERE id_pago = %s", (id_pago,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensaje': 'Pago eliminado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ REEMBOLSOS ============

# EDITAR REEMBOLSO
@app.route('/api/reembolsos/<int:id_reembolso>', methods=['PUT'])
def actualizar_estado_reembolso(id_reembolso):
    if not session.get('es_admin'):
        return jsonify({'error': 'No autorizado'}), 403
    try:
        data = request.get_json()
        nuevo_estado = data.get('estado')
        nuevo_motivo = data.get('motivo')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Si solo se actualiza el estado (aprobar/rechazar)
        if nuevo_estado and not nuevo_motivo:
            cursor.execute("""
                UPDATE reembolsos 
                SET estado_reembolso = %s 
                WHERE id_reembolso = %s
            """, (nuevo_estado, id_reembolso))
        # Si se edita todo (motivo + estado)
        else:
            cursor.execute("""
                UPDATE reembolsos 
                SET motivo = %s, estado_reembolso = %s 
                WHERE id_reembolso = %s
            """, (nuevo_motivo, nuevo_estado, id_reembolso))
        
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensaje': 'Reembolso actualizado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ELIMINAR REEMBOLSO
@app.route('/api/reembolsos/<int:id_reembolso>', methods=['DELETE'])
def eliminar_reembolso(id_reembolso):
    if not session.get('es_admin'):
        return jsonify({'error': 'No autorizado'}), 403
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reembolsos WHERE id_reembolso = %s", (id_reembolso,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensaje': 'Reembolso eliminado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# =========================
# EJECUCIÓN
# =========================
if __name__ == '__main__':
    app.run(debug=True)
