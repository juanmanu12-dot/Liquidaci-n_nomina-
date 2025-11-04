from flask import Flask, render_template, request
from src.model import liquidacion

app = Flask(__name__, template_folder="templates")

@app.route("/")
def hello():
    return render_template("compra.html")

@app.route("/calcular_cuota")
def calcular_cuota():
    salario = float(request.args["salario"])
    dias = int(request.args["dias"])
    honocturnas = int(request.args.get("honocturnas", 0))
    hodominicales = int(request.args.get("hodominicales", 0))
    transporte = float(request.args.get("transporte", 0))

    empleado_id = 1

    liquidacion_id = liquidacion.registrar_liquidacion(
        empleado_id=empleado_id,
        salario_mensual=salario,
        dias_trabajados=dias,
        horas_extra_diurnas=0,
        horas_extra_nocturnas=honocturnas,
        horas_extra_dominicales=hodominicales,
        aplica_auxilio_transporte=(transporte > 0)
    )

    return render_template("resultado.html", total=liquidacion_id)

if __name__ == "__main__":
    app.run(debug=True)
