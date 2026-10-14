from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, render_template, request
from sqlalchemy.exc import IntegrityError

from .auth import login_required
from .extensions import db
from .models import Producto

inventory_bp = Blueprint("inventory", __name__)


def _product_data(data):
    try:
        stock = int(data.get("stock", 0))
        stock_maximo = int(data.get("stock_maximo", 100))
        precio = Decimal(str(data.get("precio", "0")))
    except (TypeError, ValueError, InvalidOperation):
        raise ValueError("Los valores numéricos no son válidos.")

    if stock < 0 or stock_maximo < 0 or precio < 0:
        raise ValueError("Stock, stock máximo y precio no pueden ser negativos.")
    if stock > stock_maximo:
        raise ValueError("El stock no puede superar el stock máximo.")

    return {
        "codigo": str(data.get("codigo", "")).strip(),
        "nombre": str(data.get("nombre", "")).strip(),
        "categoria": str(data.get("categoria", "")).strip(),
        "descripcion": str(data.get("descripcion", "")).strip(),
        "medidas": str(data.get("medidas", "")).strip(),
        "stock": stock,
        "stock_maximo": stock_maximo,
        "precio": precio,
    }


def _validate_required(data):
    for field in ("codigo", "nombre", "categoria"):
        if not data[field]:
            raise ValueError(f"El campo '{field}' es obligatorio.")


@inventory_bp.route("/inventario")
@login_required
def inventario():
    productos = Producto.query.order_by(Producto.nombre.asc()).all()
    total_prod = len(productos)
    stock_bajo = sum(
        1 for p in productos if p.stock > 0 and p.stock_maximo > 0 and p.stock < p.stock_maximo * 0.2
    )
    sin_stock = sum(1 for p in productos if p.stock == 0)
    categorias = len({p.categoria for p in productos})
    valor_inv = sum((p.stock * p.precio for p in productos), Decimal("0.00"))

    return render_template(
        "inventario.html",
        productos=productos,
        total_prod=total_prod,
        stock_bajo=stock_bajo,
        sin_stock=sin_stock,
        categorias=categorias,
        valor_inv=valor_inv,
    )


@inventory_bp.route("/productos")
@login_required
def productos():
    todos = Producto.query.order_by(Producto.nombre.asc()).all()
    categorias = sorted({p.categoria for p in todos}, key=str.lower)
    return render_template("productos.html", productos=todos, categorias=categorias)


@inventory_bp.route("/api/productos", methods=["POST"])
@login_required
def add_producto():
    data = request.get_json(silent=True) or {}
    try:
        values = _product_data(data)
        _validate_required(values)
        nuevo = Producto(**values)
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"status": "ok", "id": nuevo.id}), 201
    except ValueError as exc:
        db.session.rollback()
        return jsonify({"status": "error", "msg": str(exc)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"status": "error", "msg": "El código ya existe."}), 409


@inventory_bp.route("/api/productos/<int:product_id>", methods=["PUT", "DELETE"])
@login_required
def update_producto(product_id):
    producto = Producto.query.get_or_404(product_id)

    if request.method == "DELETE":
        db.session.delete(producto)
        db.session.commit()
        return jsonify({"status": "ok"})

    data = request.get_json(silent=True) or {}
    try:
        values = _product_data(data)
        _validate_required(values)
        for key, value in values.items():
            setattr(producto, key, value)
        db.session.commit()
        return jsonify({"status": "ok"})
    except ValueError as exc:
        db.session.rollback()
        return jsonify({"status": "error", "msg": str(exc)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"status": "error", "msg": "El código ya existe."}), 409
