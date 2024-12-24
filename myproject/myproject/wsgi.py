"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask
from dashboard_app.dash_app import create_dash_app

# สร้าง Flask Server
flask_server = Flask(__name__)

# สร้าง Dash App บน Flask Server
create_dash_app(flask_server)

# รวม Django และ Dash
application = DispatcherMiddleware(
    get_wsgi_application(),  # Django WSGI App
    {'/dash': flask_server}  # เส้นทาง Dash
)
