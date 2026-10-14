-- =========================================================
-- BASE DE DATOS: FERRETERIA
-- Esquema inicial para la aplicación Flask
-- =========================================================

CREATE DATABASE IF NOT EXISTS ferreteria
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE ferreteria;

-- =========================================================
-- TABLA: usuario
-- =========================================================

CREATE TABLE IF NOT EXISTS usuario (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'admin',

    CONSTRAINT uq_usuario_username
        UNIQUE (username)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;


-- =========================================================
-- TABLA: producto
-- =========================================================

CREATE TABLE IF NOT EXISTS producto (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    codigo VARCHAR(100) NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    categoria VARCHAR(100) NOT NULL,

    descripcion TEXT NULL,
    medidas VARCHAR(100) NULL,

    stock INT NOT NULL DEFAULT 0,
    stock_maximo INT NOT NULL DEFAULT 100,

    precio DECIMAL(10,2) NOT NULL DEFAULT 0.00,

    CONSTRAINT uq_producto_codigo
        UNIQUE (codigo),

    CONSTRAINT chk_producto_stock
        CHECK (stock >= 0),

    CONSTRAINT chk_producto_stock_maximo
        CHECK (stock_maximo >= 0),

    CONSTRAINT chk_producto_stock_limite
        CHECK (stock <= stock_maximo),

    CONSTRAINT chk_producto_precio
        CHECK (precio >= 0),

    INDEX idx_producto_categoria (categoria),
    INDEX idx_producto_nombre (nombre)

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;


-- =========================================================
-- TABLA: venta
-- =========================================================

CREATE TABLE IF NOT EXISTS venta (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    producto_id INT UNSIGNED NOT NULL,

    cantidad INT NOT NULL,

    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_venta_cantidad
        CHECK (cantidad > 0),

    CONSTRAINT fk_venta_producto
        FOREIGN KEY (producto_id)
        REFERENCES producto(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    INDEX idx_venta_producto (producto_id),
    INDEX idx_venta_fecha (fecha)

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;
