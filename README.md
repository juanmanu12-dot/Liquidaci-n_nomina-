#  Liquidación de Nómina

##  ¿Qué es la liquidación de nómina?

La liquidación de nómina es el proceso administrativo mediante el cual una empresa calcula y paga de manera correcta las remuneraciones a sus empleados, cumpliendo con las obligaciones laborales y legales establecidas.

Este proyecto está diseñado para automatizar y facilitar el cálculo de la nómina, permitiendo registrar y procesar de forma precisa elementos como:

* Sueldo base
* Horas extra (diurnas, nocturnas, dominicales/festivas)
* Auxilio de transporte
* Deducciones obligatorias (salud y pensión)
* Aportes del empleador
* Provisiones (cesantías, prima, vacaciones, intereses a las cesantías)

La aplicación no solo reduce errores humanos y el tiempo invertido en tareas administrativas, sino que también asegura el cumplimiento de las normativas laborales y tributarias vigentes en cada país.

---

##  Fórmulas empleadas

### 1. Valor hora

```
valor_hora = salario / (30 * 8)
```

### 2. Horas extra

* Extra diurna:

```
extra_d = horas_extra_d * valor_hora * 1.25
```

* Extra nocturna:

```
extra_n = horas_extra_n * valor_hora * 1.75
```

* Extra dominical/festiva:

```
extra_dom = horas_extra_dom * valor_hora * 2
```

### 3. Salario proporcional a días trabajados

```
salario_base = salario * dias / 30
```

### 4. Auxilio de transporte

```
aux = 162000 (si aplica)
```

### 5. Total ingresos

```
total_ingresos = salario_base + aux + extra_d + extra_n + extra_dom
```

### 6. Deducciones (empleado)

```
salud = salario_base * 0.04
pension = salario_base * 0.04
deducciones = salud + pension
```

### 7. Neto a pagar

```
neto = total_ingresos - deducciones
```

### 8. Provisiones (prestaciones sociales)

```
cesantias = salario * dias / 360
intereses = cesantias * 0.12
prima = salario * dias / 360
vacaciones = salario * dias / 720
total_provisiones = cesantias + intereses + prima + vacaciones
```

### 9. Aportes del empleador

```
salud = salario * 0.085
pension = salario * 0.12
ARL = salario * 0.0052
caja = salario * 0.04
ICBF = salario * 0.03
SENA = salario * 0.02
total_aportes = salud + pension + ARL + caja + ICBF + SENA
```

---
## Requisitos previos
* se necesita Python 3.8+ instalado.
*Sistema operativo Windows, Linux o MacOS

## instrucciones de uso
-clonar el repositorio:https://github.com/juanmanu12-dot/Liquidaci-n_nomina-.git -Entrar al proyecto: Liquidaci-n_nomina- -Ejecutar el programa:python main.py -Ejecutar pruebas unitarias: python -m unittest discover

## Cómo ejecutar la aplicación en consola
1.Abre la terminal en Visual Studio Code.
2.Navega a la carpeta raíz del proyecto:

```bash
cd "Liquidaci-n_nomina-" (entras a la carpeta principal)
```
3.Ejecuta el archivo principal de la interfaz

```bash
python src/view/interfaz.py
```

4.Ingresa los datos solicitados en la consola para simular la liquidacion de nomina 
Esto iniciará la interfaz de consola y podrás realizar simulaciones directamente desde la terminal

## Cómo ejecutar los tests

1.Abre la terminal ya sea en Visual Studio Code o usando cmd.
2.Navega a la carpeta del proyecto(Por Ejemplo):
```bash
cmd
cd "Liquidaci-n_nomina-"
```

3.Ejecuta el archivo de test con unittest:
cmd
py test/test_Liquidaci-n_nomina-.py


Para ejecutar las pruebas, desde la raíz del proyecto:

```bash
py  test/ pruebas.py
```
Esto ejecutará todas las pruebas y mostrará los resultados



##  Beneficios del proyecto

* Automatiza el cálculo de nómina.
* Reduce errores humanos.
* Cumple con normativas laborales vigentes.
* Permite pruebas automatizadas para asegurar la precisión de los cálculos.

## Integrantes 

* moises Joshua Herrera Galindo 
* Nicol Valeria Atehortua Atehortua 
* Francisco Gomes Gomes





