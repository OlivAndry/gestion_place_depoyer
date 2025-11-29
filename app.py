from flask import Flask, render_template
from models.database import init_db
from controllers.invitee_controller import invitee_bp
from controllers.table_controller import table_bp
from controllers.placement_controller import placement_bp
import os

app = Flask(__name__)

# Configuration depuis Render (variables d'environnement)
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")

mysql = init_db(app)

# Enregistrement des blueprints
app.register_blueprint(invitee_bp)
app.register_blueprint(table_bp)
app.register_blueprint(placement_bp)

@app.route('/')
def home():
    return render_template('accueil.html')

# IMPORTANT : ne pas lancer app.run() sur Render
# Render utilisera gunicorn automatiquement
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
