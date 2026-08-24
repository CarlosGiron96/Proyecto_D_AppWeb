from flask import Flask, render_template

app = Flask(__name__)

# Ruta principal (mantiene el index.html informativo)
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el módulo de Productos
@app.route('/productos')
def productos():
    # Datos de ejemplo para renderizar dinámicamente
    lista_productos = [
        {"id": 101, "nombre": "Café Arábigo (Loja)", "origen": "Loja", "precio": 8.50, "stock": 45},
        {"id": 102, "nombre": "Café Robusta (Amazonía)", "origen": "Amazonía", "precio": 6.00, "stock": 30},
        {"id": 103, "nombre": "Blend Tradicional (Manabí)", "origen": "Manabí", "precio": 7.25, "stock": 60}
    ]
    return render_template('productos.html', productos=lista_productos)

# Ruta para el módulo de Clientes
@app.route('/clientes')
def clientes():
    lista_clientes = [
        {"id": 1, "nombre": "Cafetería El Aroma", "ciudad": "Quito", "contacto": "0991234567"},
        {"id": 2, "nombre": "Distribuidora del Sur", "ciudad": "Guayaquil", "contacto": "0987654321"}
    ]
    return render_template('clientes.html', clientes=lista_clientes)

# Ruta para el módulo de Proveedores
@app.route('/proveedores')
def proveedores():
    lista_proveedores = [
        {"id": 1, "finca": "Finca Santa Rosa", "region": "Loja", "tipo_grano": "Arábigo"},
        {"id": 2, "finca": "Asociación Manabí Gourmet", "region": "Manabí", "tipo_grano": "Blend"}
    ]
    return render_template('proveedores.html', proveedores=lista_proveedores)

# Ruta para el módulo de Facturación
@app.route('/facturacion')
def facturacion():
    lista_facturas = [
        {"nro": "FAC-001", "cliente": "Cafetería El Aroma", "fecha": "2026-08-10", "total": 170.00, "estado": "Pagada"},
        {"nro": "FAC-002", "cliente": "Distribuidora del Sur", "fecha": "2026-08-15", "total": 362.50, "estado": "Pendiente"}
    ]
    return render_template('facturacion.html', facturas=lista_facturas)

if __name__ == '__main__':
    app.run(debug=True)