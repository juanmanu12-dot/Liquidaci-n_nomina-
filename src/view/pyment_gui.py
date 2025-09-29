from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

import sys
sys.path.append("src")
from src.model.liquidacion import (calcular_neto_a_pagar,
    calcular_provisiones,
    calcular_aportes_empleador)

class NominaApp(App):
    def build(self):
        contenedor = GridLayout(cols=2, padding=20, spacing=20)

        contenedor.add_widget(Label(text="Salario mensual"))
        self.salario = TextInput(font_size=24)
        contenedor.add_widget(self.salario)

        contenedor.add_widget(Label(text="Días trabajados"))
        self.dias = TextInput(font_size=24)
        contenedor.add_widget(self.dias)

        contenedor.add_widget(Label(text="Horas extra diurnas"))
        self.he_diurnas = TextInput(font_size=24)
        contenedor.add_widget(self.he_diurnas)

        contenedor.add_widget(Label(text="Horas extra nocturnas"))
        self.he_nocturnas = TextInput(font_size=24)
        contenedor.add_widget(self.he_nocturnas)

        contenedor.add_widget(Label(text="Horas extra dominicales"))
        self.he_dominicales = TextInput(font_size=24)
        contenedor.add_widget(self.he_dominicales)

        contenedor.add_widget(Label(text="¿Aplica auxilio transporte? (1=Sí, 0=No)"))
        self.aux = TextInput(font_size=24)
        contenedor.add_widget(self.aux)

        self.resultado = Label()
        contenedor.add_widget(self.resultado)

        calcular = Button(text="Calcular Nómina", font_size=30)
        contenedor.add_widget(calcular)

        calcular.bind(on_press=self.calcular_nomina)

        return contenedor

    def calcular_nomina(self, sender):
        try:
            self.validar()

            salario = float(self.salario.text)
            dias = int(self.dias.text)
            he_d = int(self.he_diurnas.text)
            he_n = int(self.he_nocturnas.text)
            he_dom = int(self.he_dominicales.text)
            aux = bool(int(self.aux.text))

          
            neto_pagar = calcular_neto_a_pagar(salario, dias, he_d, he_n, he_dom, aux)
            valor_provisiones = calcular_provisiones(salario, dias)
            valor_aportes = calcular_aportes_empleador(salario)

            self.resultado.text = (
                f"Neto a pagar: ${neto_pagar:,.2f}\n"
                f"Provisiones: ${valor_provisiones:,.2f}\n"
                f"Aportes empleador: ${valor_aportes:,.2f}"
            )

        except ValueError:
            self.resultado.text = "Error: Los valores ingresados no son válidos."
        except Exception as err:
            self.mostrar_error(err)

    def mostrar_error(self, err):
        contenido = GridLayout(cols=1)
        contenido.add_widget(Label(text=str(err)))
        cerrar = Button(text="Cerrar")
        contenido.add_widget(cerrar)
        popup = Popup(title="Error", content=contenido)
        cerrar.bind(on_press=popup.dismiss)
        popup.open()

    def validar(self):
        if not self.salario.text.replace(".", "").isdigit():
            raise Exception("El salario debe ser un número válido.")
        if not self.dias.text.isnumeric():
            raise Exception("Los días trabajados deben ser un número válido.")
        if not self.he_diurnas.text.isnumeric():
            raise Exception("Las horas extra diurnas deben ser un número válido.")
        if not self.he_nocturnas.text.isnumeric():
            raise Exception("Las horas extra nocturnas deben ser un número válido.")
        if not self.he_dominicales.text.isnumeric():
            raise Exception("Las horas extra dominicales deben ser un número válido.")
        if self.aux.text not in ["0", "1"]:
            raise Exception("Auxilio transporte debe ser 1 (sí) o 0 (no).")


if __name__ == "__main__":
    NominaApp().run()
