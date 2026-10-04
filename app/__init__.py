from flask import Flask

from .extensions import db
from .auth import auth_bp
from .inventory import inventory_bp
from .sales import sales_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(sales_bp)

    @app.route("/")
    def index():
        from flask import redirect, session, url_for
        if "user_id" in session:
            return redirect(url_for("inventory.inventario"))
        return redirect(url_for("auth.login"))

    return app
