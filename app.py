import os
from flask import Flask, render_template
from dotenv import load_dotenv
from app.controllers.auth_controller import auth_bp

load_dotenv()

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(auth_bp)

@app.route("/")
def inicio():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
    
