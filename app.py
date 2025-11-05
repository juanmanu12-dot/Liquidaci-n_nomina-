# --------------------------------------------
# app.py — Sistema Web de Liquidación de Nómina
# --------------------------------------------
from flask import Flask, render_template, request, redirect, url_for
import os
from src.model.liquidacion import registrar_liquidacion
from src.model.empleado import Empleado  # <-- IMPORTANTE: Añadido

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


# ------------------- RUTA USUARIOS (CORREGIDA) -------------------
@app.route("/usuarios")
def usuarios():
    print("✅ Entrando en /usuarios (listando)")
    try:
        # 1. Llama a la función del modelo para obtener los empleados
        lista_empleados = Empleado.listar()
        
        # 2. Envía la lista al HTML (plantilla)
        return render_template("usuarios.html", empleados=lista_empleados, error=None)
    
    except Exception as e:
        print(f"❌ Error al listar empleados: {e}")
        # Envía una lista vacía y un error si falla
        return render_template("usuarios.html", empleados=[], error=str(e))


# ------------------- RUTA NUEVO USUARIO (NUEVA) -------------------
@app.route("/usuarios/nuevo", methods=["GET", "POST"])
def nuevo_usuario():
    
    if request.method == 'POST':
        # Si el formulario se envió (POST), procesamos los datos
        try:
            # 1. Recoger datos del formulario (debe coincidir con el HTML)
            nombre = request.form['nombre']
            cargo = request.form['cargo']
            salario = float(request.form['salario'])
            
            # 2. Llamar a la función del modelo (probada con pytest)
            Empleado.insertar(nombre, cargo, salario)
            print(f"✅ Empleado '{nombre}' insertado.")
            
            # 3. Redirigir de vuelta a la lista de usuarios
            return redirect(url_for('usuarios')) 
    
        except Exception as e:
            print(f"❌ Error al crear usuario: {e}")
            # Vuelve a mostrar el formulario con un mensaje de error
            return render_template("usuario_formulario.html", error=str(e))
    
    # Si es GET, solo muestra el formulario para crear
    print("✅ Mostrando formulario para nuevo usuario...")
    return render_template("usuario_formulario.html", error=None)


# ------------------- RUTA CREAR TABLAS -------------------
@app.route("/crear_tablas")
def crear_tablas():
    print("✅ Entrando en /crear_tablas")
    return "<h3>Tablas creadas correctamente ✅</h3>"


# ------------------- MAIN -------------------
if __name__ == "__main__":
    app.run(debug=True)