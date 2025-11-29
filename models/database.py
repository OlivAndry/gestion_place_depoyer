from flask_mysqldb import MySQL
from config.config import Config

mysql = MySQL()

def init_db(app):
    app.config['MYSQL_HOST'] = Config.MYSQL_HOST
    app.config['MYSQL_USER'] = Config.MYSQL_USER
    app.config['MYSQL_PASSWORD'] = Config.MYSQL_PASSWORD
    app.config['MYSQL_DB'] = Config.MYSQL_DB
    app.config['MYSQL_CURSORCLASS'] = Config.MYSQL_CURSORCLASS

    mysql.init_app(app)
    return mysql
