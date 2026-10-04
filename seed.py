import os
import sys

from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import Usuario


def main():
    username = os.getenv("ADMIN_USERNAME", "admin")
    password = os.getenv("ADMIN_PASSWORD")
    if not password:
        print("ERROR: define ADMIN_PASSWORD antes de ejecutar seed.py")
        sys.exit(1)

    app = create_app()
    with app.app_context():
        user = Usuario.query.filter_by(username=username).first()
        if user:
            print(f"El usuario '{username}' ya existe.")
            return
        db.session.add(
            Usuario(username=username, password=generate_password_hash(password), rol="admin")
        )
        db.session.commit()
        print(f"Usuario '{username}' creado correctamente.")


if __name__ == "__main__":
    main()
