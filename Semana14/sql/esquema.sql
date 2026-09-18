CREATE DATABASE IF NOT EXISTS cocoffe_db;
USE cocoffe_db;

-- Tabla Proveedores
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

-- Tabla Productos (Con FK a Proveedores)
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    origen VARCHAR(100) NOT NULL,
    id_proveedor INT,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE SET NULL
);

-- Tabla Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cedula VARCHAR(13) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

-- Tabla Facturas
CREATE TABLE IF NOT EXISTS facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- Insertar proveedor por defecto para pruebas
INSERT INTO proveedores (nombre, telefono, correo) 
VALUES ('Asociación de Caficultores de Loja', '0991234567', 'contacto@cafeloja.ec')
ON DUPLICATE KEY UPDATE id_proveedor=id_proveedor;