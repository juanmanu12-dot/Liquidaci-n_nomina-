import sys
sys.path.append("src")

import unittest

from src.model import liquidacion


# Helpers para calcular los esperados según el nuevo test
def esperado_neto(salario, dias, h_extra_d, h_extra_n, h_extra_dom, aplica_aux):
    valor_hora = liquidacion.calcular_valor_hora(salario)
    extra_d = h_extra_d * valor_hora * 1.25
    extra_n = h_extra_n * valor_hora * 1.75
    extra_dom = h_extra_dom * valor_hora * 2
    salario_base = salario * dias / 30
    aux = liquidacion.AUX_TRANSPORTE if aplica_aux else 0
    total_ingresos = salario_base + aux + extra_d + extra_n + extra_dom
    deducciones = salario_base * liquidacion.PORC_SALUD + salario_base * liquidacion.PORC_PENSION
    return total_ingresos - deducciones


def esperado_provisiones(salario, dias):
    cesantias = salario * dias / 360
    intereses = cesantias * 0.12
    prima = salario * dias / 360
    vacaciones = salario * dias / 720
    return cesantias + intereses + prima + vacaciones


def esperado_aportes_empleador(salario):
    salud = salario * liquidacion.PORC_SALUD_EMP
    pension = salario * liquidacion.PORC_PENSION_EMP
    arl = salario * liquidacion.PORC_ARL
    caja = salario * liquidacion.PORC_CAJA
    icbf = salario * liquidacion.PORC_ICBF
    sena = salario * liquidacion.PORC_SENA
    return salud + pension + arl + caja + icbf + sena


class TestLiquidacionNomina(unittest.TestCase):

    # CASOS NORMALES

    def test_caso_normal_1(self):
        # 10 horas extra nocturnas ≈ 109,375 para salario 1'500,000
        salario, dias = 1_500_000, 30
        h_d, h_n, h_dom, aplica_aux = 0, 10, 0, True

        self.assertAlmostEqual(
            liquidacion.calcular_neto_a_pagar(salario, dias, h_d, h_n, h_dom, aplica_aux),
            esperado_neto(salario, dias, h_d, h_n, h_dom, aplica_aux), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_provisiones(salario, dias),
            esperado_provisiones(salario, dias), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_aportes_empleador(salario),
            esperado_aportes_empleador(salario), places=2
        )

    def test_caso_normal_2(self):
        salario, dias = 1_200_000, 30
        h_d, h_n, h_dom, aplica_aux = 0, 10, 0, True  # ~87,500 de extra nocturna

        self.assertAlmostEqual(
            liquidacion.calcular_neto_a_pagar(salario, dias, h_d, h_n, h_dom, aplica_aux),
            esperado_neto(salario, dias, h_d, h_n, h_dom, aplica_aux), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_provisiones(salario, dias),
            esperado_provisiones(salario, dias), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_aportes_empleador(salario),
            esperado_aportes_empleador(salario), places=2
        )

    def test_caso_normal_3(self):
        salario, dias = 2_000_000, 30
        h_d, h_n, h_dom, aplica_aux = 0, 12, 0, False  # ~175,000 extra nocturna, sin aux

        self.assertAlmostEqual(
            liquidacion.calcular_neto_a_pagar(salario, dias, h_d, h_n, h_dom, aplica_aux),
            esperado_neto(salario, dias, h_d, h_n, h_dom, aplica_aux), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_provisiones(salario, dias),
            esperado_provisiones(salario, dias), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_aportes_empleador(salario),
            esperado_aportes_empleador(salario), places=2
        )

    def test_caso_normal_4(self):
        salario, dias = 980_000, 30
        h_d, h_n, h_dom, aplica_aux = 0, 6, 0, True  # algunas extras + aux

        self.assertAlmostEqual(
            liquidacion.calcular_neto_a_pagar(salario, dias, h_d, h_n, h_dom, aplica_aux),
            esperado_neto(salario, dias, h_d, h_n, h_dom, aplica_aux), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_provisiones(salario, dias),
            esperado_provisiones(salario, dias), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_aportes_empleador(salario),
            esperado_aportes_empleador(salario), places=2
        )

    # CASOS EXTRAORDINARIOS
    def test_caso_extraordinario_1(self):
        # Sin extras ni aux
        salario, dias = 1_500_000, 30
        h_d, h_n, h_dom, aplica_aux = 0, 0, 0, False

        self.assertAlmostEqual(
            liquidacion.calcular_neto_a_pagar(salario, dias, h_d, h_n, h_dom, aplica_aux),
            esperado_neto(salario, dias, h_d, h_n, h_dom, aplica_aux), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_provisiones(salario, dias),
            esperado_provisiones(salario, dias), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_aportes_empleador(salario),
            esperado_aportes_empleador(salario), places=2
        )

    def test_caso_extraordinario_2(self):
        # 15 días, pocas extras, sin aux
        salario, dias = 1_000_000, 15
        h_d, h_n, h_dom, aplica_aux = 0, 5, 0, False

        self.assertAlmostEqual(
            liquidacion.calcular_neto_a_pagar(salario, dias, h_d, h_n, h_dom, aplica_aux),
            esperado_neto(salario, dias, h_d, h_n, h_dom, aplica_aux), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_provisiones(salario, dias),
            esperado_provisiones(salario, dias), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_aportes_empleador(salario),
            esperado_aportes_empleador(salario), places=2
        )

    def test_caso_extraordinario_3(self):
        # Extras dominicales
        salario, dias = 2_000_000, 30
        h_d, h_n, h_dom, aplica_aux = 0, 0, 8, False

        self.assertAlmostEqual(
            liquidacion.calcular_neto_a_pagar(salario, dias, h_d, h_n, h_dom, aplica_aux),
            esperado_neto(salario, dias, h_d, h_n, h_dom, aplica_aux), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_provisiones(salario, dias),
            esperado_provisiones(salario, dias), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_aportes_empleador(salario),
            esperado_aportes_empleador(salario), places=2
        )

    def test_caso_extraordinario_4(self):
        # 20 días, sin extras, sin aux
        salario, dias = 1_200_000, 20
        h_d, h_n, h_dom, aplica_aux = 0, 0, 0, False

        self.assertAlmostEqual(
            liquidacion.calcular_neto_a_pagar(salario, dias, h_d, h_n, h_dom, aplica_aux),
            esperado_neto(salario, dias, h_d, h_n, h_dom, aplica_aux), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_provisiones(salario, dias),
            esperado_provisiones(salario, dias), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_aportes_empleador(salario),
            esperado_aportes_empleador(salario), places=2
        )

    # CASOS DE ERROR

    def test_caso_error_1(self):
        # Horas negativas (el nuevo liquidacion.py no lanza error: verifica el cálculo)
        salario, dias = 1_500_000, 30
        h_d, h_n, h_dom, aplica_aux = 0, -5, 0, True

        self.assertAlmostEqual(
            liquidacion.calcular_neto_a_pagar(salario, dias, h_d, h_n, h_dom, aplica_aux),
            esperado_neto(salario, dias, h_d, h_n, h_dom, aplica_aux), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_provisiones(salario, dias),
            esperado_provisiones(salario, dias), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_aportes_empleador(salario),
            esperado_aportes_empleador(salario), places=2
        )

    def test_caso_error_2(self):
        # Más de 30 días (el nuevo liquidacion.py lo toma proporcional)
        salario, dias = 1_200_000, 31
        h_d, h_n, h_dom, aplica_aux = 0, 4, 0, True

        self.assertAlmostEqual(
            liquidacion.calcular_neto_a_pagar(salario, dias, h_d, h_n, h_dom, aplica_aux),
            esperado_neto(salario, dias, h_d, h_n, h_dom, aplica_aux), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_provisiones(salario, dias),
            esperado_provisiones(salario, dias), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_aportes_empleador(salario),
            esperado_aportes_empleador(salario), places=2
        )

    def test_caso_error_3(self):
        # Salario alto con aux=True (el nuevo liquidacion.py paga aux si se indica)
        salario, dias = 2_000_000, 30
        h_d, h_n, h_dom, aplica_aux = 5, 5, 5, True

        self.assertAlmostEqual(
            liquidacion.calcular_neto_a_pagar(salario, dias, h_d, h_n, h_dom, aplica_aux),
            esperado_neto(salario, dias, h_d, h_n, h_dom, aplica_aux), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_provisiones(salario, dias),
            esperado_provisiones(salario, dias), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_aportes_empleador(salario),
            esperado_aportes_empleador(salario), places=2
        )

    def test_caso_error_4(self):
        # Salario 0, días 0 (todo en 0)
        salario, dias = 1_000_000, 0
        h_d, h_n, h_dom, aplica_aux = 0, 0, 0, False

        self.assertAlmostEqual(
            liquidacion.calcular_neto_a_pagar(0, dias, h_d, h_n, h_dom, aplica_aux),
            esperado_neto(0, dias, h_d, h_n, h_dom, aplica_aux), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_provisiones(0, dias),
            esperado_provisiones(0, dias), places=2
        )
        self.assertAlmostEqual(
            liquidacion.calcular_aportes_empleador(0),
            esperado_aportes_empleador(0), places=2
        )



if __name__ == '__main__':
    unittest.main()
