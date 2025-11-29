from flask import Flask, render_template
from models.database import init_db
from controllers.invitee_controller import invitee_bp
from controllers.table_controller import table_bp
from controllers.placement_controller import placement_bp

app = Flask(__name__)
mysql = init_db(app)

# Activer les routes du controller
app.register_blueprint(invitee_bp)
app.register_blueprint(table_bp)
app.register_blueprint(placement_bp)

@app.route('/')
def home():
    return render_template('accueil.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
