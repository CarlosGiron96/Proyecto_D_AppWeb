import os
import sqlite3
from flask import Flask, render_template, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cocoffe_secret_key_2026'

# Ruta para guardar la BD localmente en /data
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'cocoffe.db')

def init_db():
    """Crea la base de datos y la tabla de productos si no existen."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            origen TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inicializar BD al arrancar
init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Para acceder a campos por nombre
    return conn

# --- MÓDULO PRODUCTOS (SQLITE) ---

@app.route('/productos')
def productos():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('productos.html', productos=productos)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        # Convierte el Decimal de WTForms a float para SQLite
        precio = float(form.precio.data)
        stock = form.stock.data
        origen = form.origen.data if hasattr(form, 'origen') else form.categoria.data

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO productos (nombre, precio, stock, origen) VALUES (?, ?, ?, ?)',
            (nombre, precio, stock, origen)
        )
        conn.commit()
        conn.close()

        flash('¡Café registrado exitosamente en la base de datos!', 'success')
        return redirect(url_for('productos')) # O 'listar_productos' según tu app.py
    
    return render_template('formulario_producto.html', form=form)

# --- OTROS MÓDULOS ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html')

@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html')

if __name__ == '__main__':
    app.run(debug=True)