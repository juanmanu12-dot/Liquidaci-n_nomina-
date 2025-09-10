
---

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

##  Ejecución de la interfaz de consola

Para correr el programa desde la raíz del proyecto, usa:

```bash
py -m src.view.interfaz
```

Esto pedirá los datos por consola y mostrará el cálculo de la nómina.

---

##  Ejecución de pruebas unitarias

Para ejecutar las pruebas, desde la raíz del proyecto:

```bash
py -m unittest test.pruebas
```

Esto validará automáticamente todos los casos normales, extraordinarios y de error.



##  Beneficios del proyecto

* Automatiza el cálculo de nómina.
* Reduce errores humanos.
* Cumple con normativas laborales vigentes.
* Permite pruebas automatizadas para asegurar la precisión de los cálculos.




