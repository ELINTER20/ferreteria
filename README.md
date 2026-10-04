# Ferretería Gaspar — versión preparada para servidor

Aplicación web de inventario y salidas de productos desarrollada con Flask + MySQL.

## Estructura

```text
Ferreteria_refactor/
├── app/
│   ├── __init__.py       # Factory de Flask y registro de blueprints
│   ├── extensions.py     # Extensiones (SQLAlchemy)
│   ├── models.py         # Modelos de base de datos
│   ├── auth.py           # Login/logout y protección de rutas
│   ├── inventory.py      # Inventario y productos
│   └── sales.py          # Salidas/ventas
├── static/
├── templates/
├── database_schema.sql
├── config.py
├── run.py
├── seed.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Instalación en Ubuntu Server

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip mysql-client
cd /ruta/Ferreteria_refactor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configura las variables de entorno basándote en `.env.example`. No subas `.env` a Git.

Para preparar la base de datos:

```bash
mysql -u root -p < database_schema.sql
```

Después crea el usuario administrador:

```bash
export ADMIN_USERNAME=admin
export ADMIN_PASSWORD='cambia-esta-contrasena'
python seed.py
```

Para probar localmente:

```bash
export FLASK_APP=run.py
flask run --host=0.0.0.0 --port=5000
```

Para producción con Gunicorn:

```bash
gunicorn --workers 2 --bind 0.0.0.0:5000 run:app
```

## Importante sobre el escáner

El escáner usa la cámara del navegador. Los navegadores modernos suelen exigir un contexto seguro (HTTPS) para permitir `getUserMedia`, salvo excepciones como `localhost`. Si los alumnos accederán mediante una IP LAN (`http://192.168.x.x:5000`), conviene configurar HTTPS en el servidor o mantener el ingreso manual del código de barras como alternativa.

## Seguridad

- Las credenciales de MySQL no están en el código.
- La clave de Flask se configura mediante `SECRET_KEY`.
- El password del administrador se genera con `generate_password_hash`.
- `.env`, entornos virtuales, bases SQLite y cachés quedan fuera de Git.

## Servicio systemd (opcional)

El archivo `deploy/ferreteria.service.example` sirve como base para ejecutar la aplicación automáticamente con Gunicorn. Antes de habilitarlo, cambia `User`, `WorkingDirectory` y `EnvironmentFile` para que coincidan con la instalación real del servidor.
