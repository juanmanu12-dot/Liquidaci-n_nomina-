import sys
import os
import unittest


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)


from src.model import liquidacion


class TestLiquidacionNomina(unittest.TestCase):


    # Pruebas de cálculo del valor de la hora

    def test_valor_hora(self):
        salario = 1_200_000
        esperado = salario / 30 / 8
        self.assertEqual(liquidacion.calcular_valor_hora(salario), esperado)

    def test_valor_hora_salario_diferente(self):
        salario = 2_400_000
        esperado = salario / 30 / 8
        self.assertEqual(liquidacion.calcular_valor_hora(salario), esperado)


    # Pruebas de cálculo del neto

    def test_neto_sin_extras_con_auxilio(self):
        salario = 1_000_000
        dias = 30
        esperado_salario_base = salario
        esperado_auxilio = liquidacion.AUX_TRANSPORTE
        esperado_deducciones = salario * liquidacion.PORC_SALUD + salario * liquidacion.PORC_PENSION
        esperado = esperado_salario_base + esperado_auxilio - esperado_deducciones

        resultado = liquidacion.calcular_neto_a_pagar(salario, dias, 0, 0, 0, True)
        self.assertAlmostEqual(resultado, esperado, places=2)

    def test_neto_sin_extras_sin_auxilio(self):
        salario = 1_000_000
        dias = 30
        esperado_salario_base = salario
        esperado_auxilio = 0
        esperado_deducciones = salario * liquidacion.PORC_SALUD + salario * liquidacion.PORC_PENSION
        esperado = esperado_salario_base + esperado_auxilio - esperado_deducciones

        resultado = liquidacion.calcular_neto_a_pagar(salario, dias, 0, 0, 0, False)
        self.assertAlmostEqual(resultado, esperado, places=2)

    def test_neto_con_extras_sin_auxilio(self):
        salario = 2_000_000
        dias = 30
        valor_hora = liquidacion.calcular_valor_hora(salario)

        pago_diurna = 2 * valor_hora * liquidacion.RECARGO_EXTRA_DIURNA
        pago_nocturna = 3 * valor_hora * liquidacion.RECARGO_EXTRA_NOCTURNA
        pago_dominical = 1 * valor_hora * liquidacion.RECARGO_EXTRA_DOMINICAL

        esperado_salario_base = salario
        esperado_total_ingresos = esperado_salario_base + pago_diurna + pago_nocturna + pago_dominical
        esperado_deducciones = salario * liquidacion.PORC_SALUD + salario * liquidacion.PORC_PENSION
        esperado = esperado_total_ingresos - esperado_deducciones

        resultado = liquidacion.calcular_neto_a_pagar(salario, dias, 2, 3, 1, False)
        self.assertAlmostEqual(resultado, esperado, places=2)

    def test_neto_con_extras_y_auxilio(self):
        salario = 2_000_000
        dias = 30
        valor_hora = liquidacion.calcular_valor_hora(salario)

        pago_diurna = 1 * valor_hora * liquidacion.RECARGO_EXTRA_DIURNA
        pago_nocturna = 1 * valor_hora * liquidacion.RECARGO_EXTRA_NOCTURNA
        pago_dominical = 1 * valor_hora * liquidacion.RECARGO_EXTRA_DOMINICAL

        esperado_salario_base = salario
        esperado_total_ingresos = (
            esperado_salario_base +
            liquidacion.AUX_TRANSPORTE +
            pago_diurna + pago_nocturna + pago_dominical
        )
        esperado_deducciones = salario * liquidacion.PORC_SALUD + salario * liquidacion.PORC_PENSION
        esperado = esperado_total_ingresos - esperado_deducciones

        resultado = liquidacion.calcular_neto_a_pagar(salario, dias, 1, 1, 1, True)
        self.assertAlmostEqual(resultado, esperado, places=2)


    # Pruebas de provisiones

    def test_provisiones_mes_completo(self):
        salario = 1_800_000
        dias = 30

        cesantias = salario * dias / liquidacion.DIVISOR_CESANTIAS
        intereses_cesantias = cesantias * liquidacion.PORC_INTERESES_CESANTIAS
        prima = salario * dias / liquidacion.DIVISOR_PRIMA
        vacaciones = salario * dias / liquidacion.DIVISOR_VACACIONES
        esperado = cesantias + intereses_cesantias + prima + vacaciones

        resultado = liquidacion.calcular_provisiones(salario, dias)
        self.assertAlmostEqual(resultado, esperado, places=2)

    def test_provisiones_parciales(self):
        salario = 2_000_000
        dias = 15

        cesantias = salario * dias / liquidacion.DIVISOR_CESANTIAS
        intereses_cesantias = cesantias * liquidacion.PORC_INTERESES_CESANTIAS
        prima = salario * dias / liquidacion.DIVISOR_PRIMA
        vacaciones = salario * dias / liquidacion.DIVISOR_VACACIONES
        esperado = cesantias + intereses_cesantias + prima + vacaciones

        resultado = liquidacion.calcular_provisiones(salario, dias)
        self.assertAlmostEqual(resultado, esperado, places=2)


    # Pruebas de aportes del empleador

    def test_aportes_empleador(self):
        salario = 1_500_000

        esperado = (
            salario * liquidacion.PORC_SALUD_EMP +
            salario * liquidacion.PORC_PENSION_EMP +
            salario * liquidacion.PORC_ARL +
            salario * liquidacion.PORC_CAJA_COMPENSACION +
            salario * liquidacion.PORC_ICBF +
            salario * liquidacion.PORC_SENA
        )

        resultado = liquidacion.calcular_aportes_empleador(salario)
        self.assertAlmostEqual(resultado, esperado, places=2)

    def test_aportes_empleador_salario_diferente(self):
        salario = 3_000_000

        esperado = (
            salario * liquidacion.PORC_SALUD_EMP +
            salario * liquidacion.PORC_PENSION_EMP +
            salario * liquidacion.PORC_ARL +
            salario * liquidacion.PORC_CAJA_COMPENSACION +
            salario * liquidacion.PORC_ICBF +
            salario * liquidacion.PORC_SENA
        )

        resultado = liquidacion.calcular_aportes_empleador(salario)
        self.assertAlmostEqual(resultado, esperado, places=2)


if __name__ == "__main__":
    unittest.main()
