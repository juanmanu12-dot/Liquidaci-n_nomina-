# --------------------------------------------
# app.py — Sistema Web de Liquidación de Nómina
# --------------------------------------------
from flask import Flask, render_template, request
import os
from src.model.liquidacion import registrar_liquidacion

# Configuración del directorio de plantillas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

# Mostrar las plantillas detectadas
print("🧩 Plantillas detectadas:", os.listdir(TEMPLATE_DIR))

# ------------------- RUTA MENÚ PRINCIPAL -------------------
@app.route("/")
def index():
    print("✅ Entrando a / (inicio)")
    return render_template("index.html")


# ------------------- RUTA CALCULAR LIQUIDACIÓN -------------------
@app.route("/calcular", methods=["GET", "POST"])
def calcular():
    print("✅ Entrando en /calcular (GET o POST)")

    if request.method == "GET":
        print("✅ Mostrando formulario de cálculo...")
        return render_template("calcular.html")

    # Procesamiento de formulario
    try:
        nombre = request.form.get("nombre")
        salario = float(request.form.get("salario", 0))
        dias = int(request.form.get("dias", 0))
        horas_d = int(request.form.get("horas_d", 0))
        horas_n = int(request.form.get("horas_n", 0))
        horas_dom = int(request.form.get("horas_dom", 0))
        aplica_aux = request.form.get("aplica_aux") == "si"

        print("📩 Datos recibidos del formulario:")
        print(nombre, salario, dias, horas_d, horas_n, horas_dom, aplica_aux)

        # Llamada a tu función de liquidación (ya probada)
        liquidacion_id = registrar_liquidacion(
            1, salario, dias, horas_d, horas_n, horas_dom, aplica_aux
        )

        return render_template(
            "resultado.html",
            id=liquidacion_id,
            nombre=nombre,
            salario=salario,
            dias=dias
        )

    except Exception as e:
        print("❌ Error en /calcular:", e)
        return render_template("calcular.html", error=str(e))


# ------------------- RUTA USUARIOS -------------------
@app.route("/usuarios")
def usuarios():
    print("✅ Entrando en /usuarios")
    return render_template("usuarios.html")


# ------------------- RUTA CREAR TABLAS -------------------
@app.route("/crear_tablas")
def crear_tablas():
    print("✅ Entrando en /crear_tablas")
    return "<h3>Tablas creadas correctamente ✅</h3>"


# ------------------- MAIN -------------------
if __name__ == "__main__":
    app.run(debug=True)
    