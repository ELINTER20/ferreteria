from datetime import datetime
from decimal import Decimal

from .extensions import db


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default="admin")


class Producto(db.Model):
    __tablename__ = "producto"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(100), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(150), nullable=False)
    categoria = db.Column(db.String(100), nullable=False, index=True)
    descripcion = db.Column(db.Text, nullable=True)
    medidas = db.Column(db.String(100), nullable=True)
    stock = db.Column(db.Integer, nullable=False, default=0)
    stock_maximo = db.Column(db.Integer, nullable=False, default=100)
    precio = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal("0.00"))

    ventas = db.relationship(
        "Venta",
        back_populates="producto",
        passive_deletes=True,
    )


class Venta(db.Model):
    __tablename__ = "venta"

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(
        db.Integer,
        db.ForeignKey("producto.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    producto = db.relationship("Producto", back_populates="ventas")
