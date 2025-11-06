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



## Cómo ejecutar la aplicación con interfaz gráfica (ejecutable .exe)

Ya se incluye un ejecutable para Windows generado con **PyInstaller**.  
No es necesario tener Python instalado para usarlo.

1. Navega a la carpeta:

```
src/view/dist/
```

2. Dentro encontrarás el archivo:

```
NominaApp.exe
```

3. Haz doble clic en `NominaApp.exe` y se abrirá la interfaz gráfica para calcular la nómina.


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

## ejecucion de la base de datos 
------

##  Beneficios del proyecto

* Automatiza el cálculo de nómina.
* Reduce errores humanos.
* Cumple con normativas laborales vigentes.
* Permite pruebas automatizadas para asegurar la precisión de los cálculos.

## Integrantes 

* moises Joshua Herrera Galindo 
* Nicol Valeria Atehortua Atehortua 
* Francisco Gomes Gomes

# 💼 Proyecto: Liquidación de Nómina

Aplicación en Python conectada a **PostgreSQL** para gestionar liquidaciones de empleados.

---

## ⚙️ Requisitos
- Python 3.10 o superior
- PostgreSQL (con extensión de Microsoft o cliente normal)
- Librerías necesarias:
  ```bash
  pip install psycopg2-binary python-dotenv



-DB_HOST=localhost.
-DB_USER=tu_usuario
-DB_PASSWORD=tu_contraseña
-DB_NAME=nombre_de_tu_base
-DB_PORT=5432

Se mostrará un menú con opciones para
Insertar una nueva liquidación.
Buscar registros existentes.
Modificar el total a pagar.

## Para filtrar los datos ingresados 

SELECT * FROM liquidacion_nomina;



##  Ejecución
```bash
  python app.py
```

##  Cómo Ejecutar la Aplicación Localmente

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local, conectándote a tu base de datos en Render.

### 1. Prerrequisitos

* Python 3.8 o superior.
* Git (para clonar el repositorio).
* Acceso a una terminal o línea de comandos.

### 2. Instalación y Configuración

1.  **Clona el repositorio (si aún no lo tienes):**
    ```bash
    git clone [https://github.com/juanmanu12-dot/Liquidaci-n_nomina-.git](https://github.com/juanmanu12-dot/Liquidaci-n_nomina-.git)
    cd Liquidaci-n_nomina-
    ```

2.  **Crea y activa un entorno virtual:**
    Esto es crucial para aislar las dependencias de tu proyecto.

    * Crea el entorno:
        ```bash
        python -m venv venv
        ```
    * Activa el entorno (en Windows/PowerShell):
        ```bash
        .\venv\Scripts\Activate
        ```
    * *(Si usas macOS/Linux)*:
        ```bash
        source venv/bin/activate
        ```

3.  **Instala las librerías:**
    Con el entorno activado, instala todas las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuración de la Base de Datos

1.  **Crea el archivo `.env`:**
    En la carpeta raíz del proyecto, crea un archivo llamado `.env` (¡empieza con un punto!).

2.  **Añade tus credenciales:**
    Copia y pega las siguientes variables de entorno de tu base de datos de Render en el archivo `.env`.

    ```
    # Credenciales de la Base de Datos en Render
    DB_HOST=dpg-d3pam78dl3ps73b1epb0-a.virginia-postgres.render.com
    DB_NAME=liquidacion_nomina
    DB_USER=empresa
    DB_PASSWORD=OWOunvMbvvOv19j8GraKpQA0T26ASrUf
    DB_PORT=5432
    DATABASE_URL=postgresql://empresa:OWOunvMbvvOv19j8GraKpQA0T26ASrUf@dpg-d3pam78dl3ps73b1epb0-a.virginia-postgres.render.com:5432/liquidacion_nomina?sslmode=require
    ```

3.  **¡Importante!** Asegúrate de que tu archivo `.gitignore` contenga la línea `.env` para evitar subir tus contraseñas a GitHub.

### 4. Ejecución e Inicialización

1.  **Inicia el servidor:**
    Ejecuta la aplicación Flask:
    ```bash
    python app.py
    ```
    Verás un mensaje en la terminal indicando que el servidor está corriendo, usualmente en `http://127.0.0.1:5000/` o `http://127.0.0.1:5001/`.

2.  **Inicializa la Base de Datos (¡Solo una vez!)**
    Para configurar tu **base de datos en blanco**, abre tu navegador y ve a la siguiente URL. Esto ejecutará el script que crea las tablas `usuarios` y `liquidaciones`.

     **`http://127.0.0.1:5001/crear_tablas`**
    *(Reemplaza `5001` por el puerto que te indique tu terminal si es diferente)*.



##Para ejecutar las pruebas ejecuta el siguiente comando 

  ```bash
  python -m pytest -s
  ``` 


    Verás un mensaje de éxito o serás redirigido al inicio.
## para ejecutar todas las pruebas dentro de la carpeta test es con el siguiente comando

    ```bash
    python -m unittest discover -s test -p "test_*.py"

    ``` 

3.  **¡Listo!**
    Ahora puedes acceder a la aplicación principal y empezar a usarla.
    
     **`http://127.0.0.1:5001/`**

