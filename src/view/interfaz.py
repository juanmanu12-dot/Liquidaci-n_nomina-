import sys
import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from src.model import liquidacion
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.properties import StringProperty, BooleanProperty
from kivy.core.window import Window

Window.size = (700, 520)


class NominaForm(BoxLayout):
    resultado_texto = StringProperty("")
    auxilio_activo = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=12, spacing=12, **kwargs)

        header = Label(text='Liquidación de nómina — Interfaz Kivy', size_hint=(1, None), height=40, bold=True)
        self.add_widget(header)

        grid = GridLayout(cols=2, row_force_default=True, row_default_height=40, spacing=8, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        grid.add_widget(Label(text='Nombre del empleado:'))
        self.nombre_input = TextInput(multiline=False)
        grid.add_widget(self.nombre_input)

        grid.add_widget(Label(text='Salario mensual:'))
        self.salario_input = TextInput(multiline=False, input_filter='float')
        grid.add_widget(self.salario_input)

        grid.add_widget(Label(text='Días trabajados:'))
        self.dias_input = TextInput(multiline=False, input_filter='int')
        grid.add_widget(self.dias_input)

        grid.add_widget(Label(text='Horas extra diurnas:'))
        self.he_diurnas = TextInput(multiline=False, input_filter='int')
        grid.add_widget(self.he_diurnas)

        grid.add_widget(Label(text='Horas extra nocturnas:'))
        self.he_nocturnas = TextInput(multiline=False, input_filter='int')
        grid.add_widget(self.he_nocturnas)

        grid.add_widget(Label(text='Horas extra dominicales:'))
        self.he_dominicales = TextInput(multiline=False, input_filter='int')
        grid.add_widget(self.he_dominicales)

        grid.add_widget(Label(text='Aplica auxilio transporte:'))
        aux_box = BoxLayout(orientation='horizontal', spacing=6)
        self.aux_checkbox = CheckBox(active=False)
        aux_box.add_widget(self.aux_checkbox)
        aux_box.add_widget(Label(text='Sí'))
        grid.add_widget(aux_box)

        # Botones
        btn_box = BoxLayout(size_hint=(1, None), height=48)
        calc_btn = Button(text='Calcular nómina', on_release=self.calcular_nomina)
        btn_box.add_widget(calc_btn)

        clear_btn = Button(text='Limpiar', on_release=self.limpiar_campos)
        btn_box.add_widget(clear_btn)

        # Resultado
        sv = ScrollView(size_hint=(1, 1))
        self.result_label = Label(text=self.resultado_texto, markup=True, size_hint_y=None, valign='top')
        self.result_label.bind(texture_size=self._update_result_height)
        sv.add_widget(self.result_label)

        self.add_widget(grid)
        self.add_widget(btn_box)
        self.add_widget(sv)

    def _update_result_height(self, instance, value):
        instance.height = instance.texture_size[1]
        instance.text_size = (self.width - 24, None)

    def limpiar_campos(self, *args):
        self.nombre_input.text = ''
        self.salario_input.text = ''
        self.dias_input.text = ''
        self.he_diurnas.text = ''
        self.he_nocturnas.text = ''
        self.he_dominicales.text = ''
        self.aux_checkbox.active = False
        self.result_label.text = ''

    def calcular_nomina(self, *args):
        try:
            nombre = self.nombre_input.text.strip() or '---'
            salario = float(self.salario_input.text) if self.salario_input.text.strip() else 0.0
            dias = int(self.dias_input.text) if self.dias_input.text.strip() else 0
            he_d = int(self.he_diurnas.text) if self.he_diurnas.text.strip() else 0
            he_n = int(self.he_nocturnas.text) if self.he_nocturnas.text.strip() else 0
            he_dom = int(self.he_dominicales.text) if self.he_dominicales.text.strip() else 0
            aux = bool(self.aux_checkbox.active)

            neto = calcular_neto_a_pagar(salario, dias, he_d, he_n, he_dom, aux)
            provisiones = calcular_provisiones(salario, dias)
            aportes = calcular_aportes_empleador(salario)

            texto = (
                f"[b]Resultados para:[/b] {nombre}\n"
                f"[b]Neto a pagar:[/b] ${neto:,.2f}\n"
                f"[b]Total provisiones:[/b] ${provisiones:,.2f}\n"
                f"[b]Aportes del empleador:[/b] ${aportes:,.2f}\n"
            )

            self.result_label.text = texto

        except ValueError:
            self.result_label.text = '[color=ff3333]Error: revisa que los campos numéricos contengan valores válidos.[/color]'
        except Exception as e:
            self.result_label.text = f'[color=ff3333]Error inesperado: {e}[/color]'


class NominaApp(App):
    def build(self):
        return NominaForm()


if __name__ == '__main__':
    NominaApp().run()
