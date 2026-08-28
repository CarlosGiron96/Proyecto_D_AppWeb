import os
from flask import Flask, render_template, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
# Configuración de Clave Secreta para CSRF
app.config['SECRET_KEY'] = 'clave_secreta_cafe_ecuador_2026'

# Almacenamiento temporal en memoria
PRODUCTOS = [
    {"id": 101, "nombre": "Café Arábigo (Loja)", "origen": "Loja", "precio": 8.50, "stock": 45},
    {"id": 102, "nombre": "Café Robusta (Amazonía)", "origen": "Amazonía", "precio": 6.00, "stock": 30}
]

CLIENTES = [
    {"id": 1, "nombre": "Cafetería El Aroma", "ciudad": "Quito", "contacto": "0991234567", "email": "aroma@mail.com"}
]

PROVEEDORES = [
    {"id": 1, "finca": "Finca Santa Rosa", "region": "Loja", "tipo_grano": "Arábigo", "telefono": "0981112233"}
]

FACTURAS = [
    {"nro": "FAC-001", "cliente": "Cafetería El Aroma", "fecha": "2026-08-10", "total": 170.00, "estado": "Pagada"}
]

@app.route('/')
def index():
    return render_template('index.html')

# MÓDULO PRODUCTOS
@app.route('/productos')
def productos():
    return render_template('productos.html', productos=PRODUCTOS)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        nuevo = {
            "id": len(PRODUCTOS) + 101,
            "nombre": form.nombre.data,
            "origen": form.origen.data,
            "precio": form.precio.data,
            "stock": form.stock.data
        }
        PRODUCTOS.append(nuevo)
        flash('Producto registrado con éxito.', 'success')
        return redirect(url_for('productos'))
    return render_template('formulario_producto.html', form=form, titulo="Nuevo Producto")

# MÓDULO CLIENTES
@app.route('/clientes')
def clientes():
    return render_template('clientes.html', clientes=CLIENTES)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevo = {
            "id": len(CLIENTES) + 1,
            "nombre": form.nombre.data,
            "ciudad": form.ciudad.data,
            "contacto": form.contacto.data,
            "email": form.email.data
        }
        CLIENTES.append(nuevo)
        flash('Cliente registrado con éxito.', 'success')
        return redirect(url_for('clientes'))
    return render_template('formulario_cliente.html', form=form, titulo="Nuevo Cliente")

# MÓDULO PROVEEDORES
@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html', proveedores=PROVEEDORES)

@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo = {
            "id": len(PROVEEDORES) + 1,
            "finca": form.finca.data,
            "region": form.region.data,
            "tipo_grano": form.tipo_grano.data,
            "telefono": form.telefono.data
        }
        PROVEEDORES.append(nuevo)
        flash('Proveedor registrado con éxito.', 'success')
        return redirect(url_for('proveedores'))
    return render_template('formulario_proveedor.html', form=form, titulo="Nuevo Proveedor")

# MÓDULO FACTURACIÓN
@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html', facturas=FACTURAS)

@app.route('/facturacion/nueva', methods=['GET', 'POST'])
def nueva_facturacion():
    form = FacturacionForm()
    if form.validate_on_submit():
        nueva = {
            "nro": f"FAC-00{len(FACTURAS) + 1}",
            "cliente": form.cliente.data,
            "fecha": str(form.fecha.data),
            "total": form.total.data,
            "estado": form.estado.data
        }
        FACTURAS.append(nueva)
        flash('Factura procesada con éxito.', 'success')
        return redirect(url_for('facturacion'))
    return render_template('formulario_facturacion.html', form=form, titulo="Nueva Factura")

if __name__ == '__main__':
    app.run(debug=True)