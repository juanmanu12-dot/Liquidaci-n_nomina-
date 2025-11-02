💼 Liquidación de Nómina
🧾 ¿Qué es la liquidación de nómina?

La liquidación de nómina es el proceso administrativo mediante el cual una empresa calcula y paga correctamente las remuneraciones a sus empleados, cumpliendo con las obligaciones laborales y legales establecidas.

Este proyecto está diseñado para automatizar y facilitar el cálculo de la nómina, permitiendo registrar y procesar de forma precisa elementos como:

Sueldo base

Horas extra (diurnas, nocturnas, dominicales/festivas)

Auxilio de transporte

Deducciones obligatorias (salud y pensión)

Aportes del empleador

Provisiones (cesantías, prima, vacaciones, intereses a las cesantías)

La aplicación reduce errores humanos, optimiza el tiempo administrativo y garantiza el cumplimiento de las normativas laborales y tributarias vigentes.

⚙️ Requisitos previos

Python 3.8+

Sistema operativo Windows, Linux o MacOS

Tener instalado PostgreSQL o acceso a una base de datos Render PostgreSQL

Instalar dependencias del proyecto:

pip install -r requirements.txt

🧮 Fórmulas empleadas
1️⃣ Valor hora
valor_hora = salario / (30 * 8)

2️⃣ Horas extra

Diurna:

extra_d = horas_extra_d * valor_hora * 1.25


Nocturna:

extra_n = horas_extra_n * valor_hora * 1.75


Dominical o festiva:

extra_dom = horas_extra_dom * valor_hora * 2

3️⃣ Salario proporcional a días trabajados
salario_base = salario * dias / 30

4️⃣ Auxilio de transporte
aux = 162000 (si aplica)

5️⃣ Total ingresos
total_ingresos = salario_base + aux + extra_d + extra_n + extra_dom

6️⃣ Deducciones (empleado)
salud = salario_base * 0.04
pension = salario_base * 0.04
deducciones = salud + pension

7️⃣ Neto a pagar
neto = total_ingresos - deducciones

8️⃣ Provisiones (prestaciones sociales)
cesantias = salario * dias / 360
intereses = cesantias * 0.12
prima = salario * dias / 360
vacaciones = salario * dias / 720
total_provisiones = cesantias + intereses + prima + vacaciones

9️⃣ Aportes del empleador
salud = salario * 0.085
pension = salario * 0.12
ARL = salario * 0.0052
caja = salario * 0.04
ICBF = salario * 0.03
SENA = salario * 0.02
total_aportes = salud + pension + ARL + caja + ICBF + SENA

🗂️ Estructura del proyecto
Liquidaci-n_nomina-
│
├── src/
│   ├── controller/
│   ├── model/
│   │   ├── liquidacion.py
│   │   ├── empleado.py
│   │   ├── database.py
│   │   └── config_db.py
│   ├── view/
│   │   └── interfaz.py
│   └── create_tables.sql
│
├── test/
│   ├── test_database.py
│   ├── test_empleado.py
│   ├── test_liquidacion.py
│   └── pruebas.py
│
├── .env
├── run_tests.py
├── requirements.txt
└── README.md

🧱 Ejecución y configuración de la base de datos
🔹 Opción 1: Base de datos externa (Render PostgreSQL)

Crea una base de datos en Render
.

Copia la cadena de conexión externa, por ejemplo:

postgresql://empresa:contraseña@dpg-xxxxx-a.virginia-postgres.render.com/liquidacion_nomina


En el archivo .env de tu proyecto, agrega:

DB_HOST=dpg-xxxxx-a.virginia-postgres.render.com
DB_NAME=liquidacion_nomina
DB_USER=empresa
DB_PASSWORD=tu_contraseña
DB_PORT=5432


En src/config_db.py asegúrate de cargar correctamente:

from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


Ejecuta el script SQL para crear las tablas:

psql < src/create_tables.sql


O usa pgAdmin:

Abre tu base de datos Render.

Copia el contenido del archivo create_tables.sql.

Pégalo en el panel SQL y ejecuta (F5).

🔹 Opción 2: Base de datos local

Si prefieres usar PostgreSQL localmente:

Crea una base de datos llamada:

CREATE DATABASE liquidacion_nomina;


Ejecuta:

psql -U postgres -d liquidacion_nomina -f src/create_tables.sql

🧪 Ejecución de pruebas unitarias

Desde la raíz del proyecto:

set PYTHONPATH=%cd%
python -m unittest discover -s test -p "test_*.py" -v


También puedes ejecutar el archivo auxiliar:

python run_tests.py


Si todo está correcto, deberías ver:

Ran 7 tests in 4.003s
OK


Entre las pruebas incluidas están:

Conexión a la base de datos (Render o local)

Creación de tablas

Registro y listado de empleados

Registro de liquidación

Cálculo de nómina y provisiones

🧭 Visualizar los datos en la base de datos

Puedes consultar los registros creados por los tests.

Con psql:
psql -h dpg-xxxxx-a.virginia-postgres.render.com -U empresa -d liquidacion_nomina


Luego dentro de PostgreSQL:

SELECT * FROM empleados;
SELECT * FROM liquidaciones;

Con pgAdmin:

Inicia sesión en tu cuenta de Render o PostgreSQL local.

Abre el panel de consultas SQL.

Ejecuta las sentencias anteriores para verificar los registros insertados por el sistema.

🧰 Cómo ejecutar la aplicación
🖥️ Consola
python src/view/interfaz.py


Se abrirá la interfaz por consola para ingresar los datos del empleado y calcular la liquidación.

💻 Interfaz gráfica (.exe)

El proyecto incluye un ejecutable generado con PyInstaller.
No se requiere Python instalado.

Ir a la carpeta:

src/view/dist/


Ejecutar:

NominaApp.exe


La aplicación se abrirá con una interfaz amigable.

🧾 Beneficios del proyecto

✅ Automatiza el cálculo de nómina
✅ Reduce errores humanos
✅ Cumple con la normatividad laboral
✅ Permite conexión con base de datos externa (Render)
✅ Incluye pruebas unitarias automáticas
✅ Cuenta con interfaz gráfica y versión ejecutable (.exe)

👨‍💻 Integrantes

Moises Joshua Herrera Galindo

Nicol Valeria Atehortua Atehortua

Francisco Gomes Gomes



