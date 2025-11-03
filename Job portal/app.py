from flask import Flask
from flask_mysqldb import MySQL
from flask_session import Session
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
Session(app)

app.extensions = getattr(app, 'extensions', {})
app.extensions['mysql'] = mysql

from auth import auth_bp
from user import user_bp
from admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)
