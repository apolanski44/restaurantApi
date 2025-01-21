from flask import Flask, render_template
from routes.TableRoutes import tables_bp
from routes.ReservationRoutes import reservations_bp
from routes.auth import auth_bp
from routes.MenuRoutes import  menu_bp

app = Flask(__name__)
app.register_blueprint(tables_bp)
app.register_blueprint(reservations_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(menu_bp)

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
