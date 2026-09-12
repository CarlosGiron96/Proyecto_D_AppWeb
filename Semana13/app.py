from flask import Flask, render_template, redirect, url_for, flash, request
from conexion.conexion import get_db_connection
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cocoffe_secret_key_2026'

# -------------------------------------------------------------------
# Módulos de Productos (CRUD Completo con MySQL)
# -------------------------------------------------------------------

@app.route('/productos')
def productos():
    """Listar todos los productos mediante SELECT + JOIN con la tabla proveedores."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) # Devuelve filas como diccionarios
    
    # Consulta con JOIN para obtener el nombre del proveedor
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
def nuevo_producto():
    """Agregar un nuevo café mediante INSERT INTO con parámetros seguras."""
    form = ProductoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        precio = float(form.precio.data)
        stock = form.stock.data
        origen = form.origen.data if hasattr(form, 'origen') else form.categoria.data
        id_proveedor = 1 # ID de proveedor por defecto

        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO productos (nombre, precio, stock, origen, id_proveedor)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nombre, precio, stock, origen, id_proveedor))
        conn.commit()
        
        cursor.close()
        conn.close()

        flash('¡Café registrado exitosamente en MySQL!', 'success')
        return redirect(url_for('productos'))
    
    return render_template('formulario_producto.html', form=form, modo="crear")


@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    """Modificar un café existente recuperando sus datos actuales mediante WHERE."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Obtener el registro a editar
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
    producto = cursor.fetchone()

    if not producto:
        cursor.close()
        conn.close()
        flash('El producto solicitado no existe.', 'danger')
        return redirect(url_for('productos'))

    form = ProductoForm()

    if request.method == 'GET':
        # Cargar los datos actuales en el formulario
        form.nombre.data = producto['nombre']
        form.precio.data = producto['precio']
        form.stock.data = producto['stock']
        if hasattr(form, 'origen'):
            form.origen.data = producto['origen']

    if form.validate_on_submit():
        nombre = form.nombre.data
        precio = float(form.precio.data)
        stock = form.stock.data
        origen = form.origen.data if hasattr(form, 'origen') else form.categoria.data

        # Actualización parametrizada con WHERE estricto
        update_query = """
            UPDATE productos 
            SET nombre = %s, precio = %s, stock = %s, origen = %s 
            WHERE id_producto = %s
        """
        cursor.execute(update_query, (nombre, precio, stock, origen, id))
        conn.commit()

        cursor.close()
        conn.close()
        flash('¡Café actualizado correctamente!', 'info')
        return redirect(url_for('productos'))

    cursor.close()
    conn.close()
    return render_template('formulario_producto.html', form=form, modo="editar", id_producto=id)


@app.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    """Eliminar un registro específico utilizando la cláusula WHERE."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    delete_query = "DELETE FROM productos WHERE id_producto = %s"
    cursor.execute(delete_query, (id,))
    conn.commit()

    cursor.close()
    conn.close()
    
    flash('El producto ha sido eliminado de la base de datos.', 'warning')
    return redirect(url_for('productos'))


# -------------------------------------------------------------------
# Otras Rutas del Sistema
# -------------------------------------------------------------------

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