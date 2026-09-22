-- Tabla 1: Usuarios (Autenticación)
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL
);

-- Tabla 2: Proveedores
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

-- Tabla 3: Productos (Relacionada con Proveedores mediante FK)
CREATE TABLE IF NOT EXISTS productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio NUMERIC(10,2) NOT NULL,
    stock INT NOT NULL,
    origen VARCHAR(100) NOT NULL,
    id_proveedor INT REFERENCES proveedores(id_proveedor) ON DELETE SET NULL
);

-- Tabla 4: Facturas (Relacionada con Usuarios mediante FK)
CREATE TABLE IF NOT EXISTS facturas (
    id_factura SERIAL PRIMARY KEY,
    id_usuario INT REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total NUMERIC(10,2) NOT NULL
);

-- Datos iniciales
INSERT INTO proveedores (nombre, telefono, correo) 
VALUES ('Asociación de Caficultores de Loja', '0991234567', 'contacto@cafeloja.ec')
ON CONFLICT DO NOTHING;