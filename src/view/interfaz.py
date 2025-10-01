import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from src.model import liquidacion  # NO toco tu import; sigue igual
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

# ================== PALETA ==================
THEME = {
    "bg":          "#0b1220",   # fondo app
    "text":        "#e5e7eb",   # texto general
    "muted":       "#a1a7b3",   # texto secundario
    "primary":     "#22d3ee",   # botones principales
    "primary_down":"#06b6d4",
    "accent":      "#a78bfa",   # botón secundario
    "accent_down": "#8b6cf2",
    "btn_text":    "#081018",
    "input_bg":    "#0f172a",   # fondo input
    "input_text":  "#e5e7eb",
    "input_cursor":"#22d3ee",
    "error":       "#f87171",
    "ok":          "#34d399",
}

def _rgba(hex_color: str, a: float = 1.0):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return (r, g, b, a)

Window.size = (700, 520)
Window.clearcolor = _rgba(THEME["bg"])  # solo color de fondo de la ventana

class NominaForm(BoxLayout):
    resultado_texto = StringProperty("")
    auxilio_activo = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=12, spacing=12, **kwargs)

        # ---------- Encabezado ----------
        header = Label(
            text='Liquidación de nómina — Interfaz Kivy',
            size_hint=(1, None),
            height=40,
            color=_rgba(THEME["accent"])  # solo color del texto
        )
        self.add_widget(header)

        # ---------- Grid de entradas ----------
        grid = GridLayout(cols=2, row_force_default=True, row_default_height=40, spacing=8, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        def _label(txt):
            # label con color consistente
            return Label(text=txt, color=_rgba(THEME["text"]))

        def _input(**kw):
            # textinput con colores (sin tocar layout)
            ti = TextInput(**kw)
            ti.background_normal = ""  # permite que background_color funcione
            ti.background_active = ""
            ti.background_color = _rgba(THEME["input_bg"])
            ti.foreground_color = _rgba(THEME["input_text"])
            ti.cursor_color = _rgba(THEME["input_cursor"])
            return ti

        grid.add_widget(_label('Nombre del empleado:'))
        self.nombre_input = _input(multiline=False)
        grid.add_widget(self.nombre_input)

        grid.add_widget(_label('Salario mensual:'))
        self.salario_input = _input(multiline=False, input_filter='float')
        grid.add_widget(self.salario_input)

        grid.add_widget(_label('Días trabajados:'))
        self.dias_input = _input(multiline=False, input_filter='int')
        grid.add_widget(self.dias_input)

        grid.add_widget(_label('Horas extra diurnas:'))
        self.he_diurnas = _input(multiline=False, input_filter='int')
        grid.add_widget(self.he_diurnas)

        grid.add_widget(_label('Horas extra nocturnas:'))
        self.he_nocturnas = _input(multiline=False, input_filter='int')
        grid.add_widget(self.he_nocturnas)

        grid.add_widget(_label('Horas extra dominicales:'))
        self.he_dominicales = _input(multiline=False, input_filter='int')
        grid.add_widget(self.he_dominicales)

        grid.add_widget(_label('Aplica auxilio transporte:'))
        aux_box = BoxLayout(orientation='horizontal', spacing=6)
        self.aux_checkbox = CheckBox(active=False)  # Kivy no cambia color fácilmente sin assets; lo dejamos default
        aux_box.add_widget(self.aux_checkbox)
        aux_box.add_widget(Label(text='Sí', color=_rgba(THEME["muted"])))
        grid.add_widget(aux_box)

        # ---------- Botones ----------
        btn_box = BoxLayout(size_hint=(1, None), height=48, spacing=8)

        def _button(txt, bg, bg_down, txt_color):
            b = Button(text=txt)
            b.background_normal = ""
            b.background_down = ""
            b.background_color = _rgba(bg)
            b.color = _rgba(txt_color)
            # mínimo feedback de click sin cambiar layout
            def on_press(_): b.background_color = _rgba(bg_down)
            def on_release(_): b.background_color = _rgba(bg)
            b.bind(on_press=on_press, on_release=on_release)
            return b

        calc_btn = _button('Calcular nómina', THEME["primary"], THEME["primary_down"], THEME["btn_text"])
        calc_btn.bind(on_release=self.calcular_nomina)
        btn_box.add_widget(calc_btn)

        clear_btn = _button('Limpiar', THEME["accent"], THEME["accent_down"], THEME["btn_text"])
        clear_btn.bind(on_release=self.limpiar_campos)
        btn_box.add_widget(clear_btn)

        # ---------- Resultado ----------
        sv = ScrollView(size_hint=(1, 1))
        self.result_label = Label(
            text=self.resultado_texto,
            markup=True,
            size_hint_y=None,
            valign='top',
            color=_rgba(THEME["text"])
        )
        self.result_label.bind(texture_size=self._update_result_height)
        sv.add_widget(self.result_label)

        # Agregar al root (mismo orden que el tuyo)
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

            # Mantengo tus llamadas tal cual (sin prefijos)
            neto = liquidacion.calcular_neto_a_pagar(salario, dias, he_d, he_n, he_dom, aux)
            provisiones = liquidacion.calcular_provisiones(salario, dias)
            aportes = liquidacion.calcular_aportes_empleador(salario)

            # Colores en el texto (markup usa hex sin #)
            ok_hex = THEME["ok"].lstrip("#")
            primary_hex = THEME["primary"].lstrip("#")

            texto = (
                f"[b]Resultados para:[/b] [color={primary_hex}]{nombre}[/color]\n"
                f"[b]Neto a pagar:[/b] [color={ok_hex}]${neto:,.2f}[/color]\n"
                f"[b]Total provisiones:[/b] ${provisiones:,.2f}\n"
                f"[b]Aportes del empleador:[/b] ${aportes:,.2f}\n"
            )
            self.result_label.text = texto

        except ValueError:
            err_hex = THEME["error"].lstrip("#")
            self.result_label.text = f'[color={err_hex}]Error: revisa que los campos numéricos contengan valores válidos.[/color]'
        except Exception as e:
            err_hex = THEME["error"].lstrip("#")
            self.result_label.text = f'[color={err_hex}]Error inesperado: {e}[/color]'


class NominaApp(App):
    def build(self):
        return NominaForm()


if __name__ == '__main__':
    NominaApp().run()


