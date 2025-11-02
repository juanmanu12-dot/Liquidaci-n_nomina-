# --------------------------------------------
# test/test_liquidacion.py — Prueba de cálculo y registro de liquidación
# --------------------------------------------
import unittest
from src.model.liquidacion import registrar_liquidacion


class TestLiquidacion(unittest.TestCase):
    """Pruebas unitarias para el módulo de liquidación."""

    def test_registro_liquidacion(self):
        print("\n💼 Probando cálculo y registro de liquidación...")
        liquidacion_id = registrar_liquidacion(
            empleado_id=1,            # ajusta según tu BD
            salario_mensual=2_500_000,
            dias_trabajados=30,
            horas_extra_diurnas=4,
            horas_extra_nocturnas=2,
            horas_extra_dominicales=1,
            aplica_auxilio_transporte=True
        )
        self.assertIsNotNone(liquidacion_id, "❌ No se registró la liquidación correctamente.")


if __name__ == "__main__":
    unittest.main()
