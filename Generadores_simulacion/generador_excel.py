import pandas as pd
import random
import faker
import os

# Inicializamos el generador de datos ficticios
fake = faker.Faker('es_CO')

# Definimos 100 filas
n = 10000

# Generamos los datos base
datos = []
for i in range(n):
    cedula = str(random.randint(1000000000, 1999999999))
    nombre = fake.name().upper()
    credito = str(random.randint(100000000000, 999999999999))
    solicitud = str(random.randint(1000000, 9999999))
    valor_prestamo = f"{random.randint(5000000, 20000000):,}".replace(",", ".")
    pagaduria = random.choice(['COLPENSIONES', 'FONDO EMPLEADOS BANCOLOMBIA', 'INVIAS', 'SECRETARÍA EDUCACIÓN', 'FNA'])
    cuotas = random.choice([60, 72, 96, 120, 144])
    valor_cuota = f"{random.randint(100000, 400000):,}".replace(",", ".")
    fecha_nacimiento = fake.date_of_birth(minimum_age=30, maximum_age=70).strftime('%d/%m/%Y')
    monto_credito = valor_prestamo
    plazo = cuotas
    valor_total_financiar = valor_prestamo
    entidad_pagadora = pagaduria
    tasa_ea = f"{round(random.uniform(18.0, 29.0), 2)}%"
    compra_cartera = f"{random.randint(1000000, 5000000):,}".replace(",", ".")
    salario = f"{random.randint(1000000, 5000000):,}".replace(",", ".")
    fecha_desprendible = fake.date_this_year().strftime('%d/%m/%Y')
    valor_total_soporte = compra_cartera
    firma_electronica = f"{nombre} - {cedula}"

    datos.append([cedula, nombre, credito, solicitud, valor_prestamo, pagaduria, cuotas, valor_cuota,
                  fecha_nacimiento, monto_credito, plazo, valor_total_financiar, entidad_pagadora,
                  tasa_ea, compra_cartera, salario, fecha_desprendible, valor_total_soporte, firma_electronica])

# Creamos el DataFrame
columnas = [
    "CEDULA", "NOMBRES", "No.CREADITO", "SOLICITUD", "Valor préstamo (crédito)", "Pagaduría",
    "Cantidad cuotas", "Valor cuota", "Fecha nacimiento", "Monto crédito (Formato conocimiento)",
    "Plazo (Formato conocimiento)", "Valor total a financiar (Amortización)",
    "Entidad pagadora (Amortización)", "Tasa E.A. (Amortización)", "Compras de cartera y prepagos",
    "Valor pensión o salario neto", "Fecha del desprendible", "Valor Total (Soporte desembolso)",
    "Firma electrónica (logo y pie)"
]

df = pd.DataFrame(datos, columns=columnas)

# Guardamos el excel en el escritorio
escritorio = os.path.join(os.path.expanduser("~"), "Desktop")  # Obtiene la ruta al escritorio
excel_path = os.path.join(escritorio, "base_simulacion_100_filas_v2.xlsx")  # Crea la ruta completa al archivo
df.to_excel(excel_path, index=False)

excel_path  # Muestra la ruta completa al archivo guardado