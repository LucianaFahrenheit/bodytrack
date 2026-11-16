import os
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from app.controllers.auth_controller import auth_bp
from app.controllers.registro_controller import reg_bp
from app.controllers.perfil_controller import perfil_bp

load_dotenv()

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
app.secret_key = os.getenv("SECRET_KEY", "troque-esta-chave")

app.register_blueprint(auth_bp)
app.register_blueprint(reg_bp)
app.register_blueprint(perfil_bp)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.errorhandler(500)
def erro_interno(e):
    return jsonify({"erro": "Erro interno no servidor. Tente novamente."}), 500


if __name__ == "__main__":
    app.run(debug=True)
