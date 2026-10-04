CREATE DATABASE IF NOT EXISTS ferreteria
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE ferreteria;

CREATE TABLE IF NOT EXISTS usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'admin'
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(100) NOT NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    descripcion TEXT NULL,
    medidas VARCHAR(100) NULL,
    stock INT NOT NULL DEFAULT 0,
    stock_maximo INT NOT NULL DEFAULT 100,
    precio DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    INDEX idx_producto_categoria (categoria)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS venta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_venta_producto (producto_id),
    INDEX idx_venta_fecha (fecha),
    CONSTRAINT fk_venta_producto
        FOREIGN KEY (producto_id) REFERENCES producto(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;
