# --------------------------------------------
# src/controller/empleado_controller.py
# --------------------------------------------
from src.model.empleado import Empleado
from src.model.liquidacion import registrar_liquidacion

class EmpleadoController:
    """Controlador para conectar vista ↔ modelo."""

    @staticmethod
    def crear_empleado(nombre, cargo, salario):
        """Registra un nuevo empleado."""
        return Empleado.insertar(nombre, cargo, salario)

    @staticmethod
    def listar_empleados():
        """Devuelve lista de empleados existentes."""
        return Empleado.listar()

    @staticmethod
    def buscar_empleado(id_empleado):
        """Busca un empleado por su ID."""
        return Empleado.buscar_por_id(id_empleado)

    @staticmethod
    def eliminar_empleado(id_empleado):
        """Elimina un empleado por su ID."""
        return Empleado.eliminar(id_empleado)

    @staticmethod
    def liquidar_empleado(id_empleado, salario, dias, h_d, h_n, h_dom, aplica_aux):
        """Genera y registra la liquidación de un empleado."""
        return registrar_liquidacion(id_empleado, salario, dias, h_d, h_n, h_dom, aplica_aux)
