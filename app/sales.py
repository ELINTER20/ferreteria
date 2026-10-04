from flask import Blueprint, jsonify, render_template, request

from .auth import login_required
from .extensions import db
from .models import Producto, Venta

sales_bp = Blueprint("sales", __name__)


@sales_bp.route("/ventas")
@login_required
def ventas():
    historial = Venta.query.order_by(Venta.fecha.desc()).all()
    return render_template("ventas.html", ventas=historial)


@sales_bp.route("/api/ventas", methods=["POST", "DELETE"])
@login_required
def manage_ventas():
    if request.method == "DELETE":
        Venta.query.delete(synchronize_session=False)
        db.session.commit()
        return jsonify({"status": "ok", "msg": "Historial eliminado"})

    data = request.get_json(silent=True) or {}
    codigo = str(data.get("codigo", "")).strip()
    try:
        cantidad = int(data.get("cantidad", 0))
    except (TypeError, ValueError):
        cantidad = 0

    if not codigo or cantidad <= 0:
        return jsonify({"status": "error", "msg": "Código y cantidad válidos son obligatorios."}), 400

    producto = Producto.query.filter_by(codigo=codigo).first()
    if not producto:
        return jsonify({"status": "error", "msg": "Producto no encontrado."}), 404
    if producto.stock < cantidad:
        return jsonify({"status": "error", "msg": "Stock insuficiente."}), 400

    producto.stock -= cantidad
    db.session.add(Venta(producto_id=producto.id, cantidad=cantidad))
    db.session.commit()
    return jsonify({"status": "ok"}), 201
