from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import get_db_connection
from models import Usuario
from forms.login_form import LoginForm
from forms.usuario_form import RegistroUsuarioForm
from forms.producto_form import ProductoForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cocoffe_secret_key_2026'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirige a /login si no está autenticado
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(user_id, get_db_connection)

# -------------------------------------------------------------------
# Rutas de Autenticación
# -------------------------------------------------------------------

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistroUsuarioForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        username = form.username.data
        # Cifrado seguro de contraseña
        password_hash = generate_password_hash(form.password.data)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO usuarios (nombre, username, password_hash) VALUES (%s, %s, %s)"
            cursor.execute(query, (nombre, username, password_hash))
            conn.commit()
            flash('¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            flash('El nombre de usuario ya existe. Por favor elige otro.', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('registro.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        usuario = Usuario.get_by_username(username, get_db_connection)

        # Validación con check_password_hash
        if usuario and check_password_hash(usuario.password_hash, password):
            login_user(usuario)
            flash(f'¡Bienvenido de nuevo, {usuario.nombre}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# -------------------------------------------------------------------
# Rutas Protegidas de Productos (CRUD MySQL)
# -------------------------------------------------------------------

@app.route('/productos')
@login_required
def productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT p.id_producto, p.nombre, p.precio, p.stock, p.origen, 
               pr.nombre AS proveedor
        FROM productos p
        LEFT JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
    """
    cursor.execute(query)
    productos_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('productos.html', productos=productos_list)


@app.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        precio = float(form.precio.data)
        stock = form.stock.data
        origen = form.origen.data if hasattr(form, 'origen') else form.categoria.data

        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO productos (nombre, precio, stock, origen, id_proveedor) VALUES (%s, %s, %s, %s, 1)"
        cursor.execute(query, (nombre, precio, stock, origen))
        conn.commit()
        cursor.close()
        conn.close()

        flash('¡Producto registrado con éxito!', 'success')
        return redirect(url_for('productos'))

    return render_template('formulario_producto.html', form=form, modo="crear")


@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
    producto = cursor.fetchone()

    if not producto:
        cursor.close()
        conn.close()
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('productos'))

    form = ProductoForm()
    if request.method == 'GET':
        form.nombre.data = producto['nombre']
        form.precio.data = producto['precio']
        form.stock.data = producto['stock']

    if form.validate_on_submit():
        precio = float(form.precio.data)
        origen = form.origen.data if hasattr(form, 'origen') else form.categoria.data
        update_query = "UPDATE productos SET nombre=%s, precio=%s, stock=%s, origen=%s WHERE id_producto=%s"
        cursor.execute(update_query, (form.nombre.data, precio, form.stock.data, origen, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Producto actualizado correctamente.', 'info')
        return redirect(url_for('productos'))

    cursor.close()
    conn.close()
    return render_template('formulario_producto.html', form=form, modo="editar", id_producto=id)


@app.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Producto eliminado de la base de datos.', 'warning')
    return redirect(url_for('productos'))


# Rutas generales
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)