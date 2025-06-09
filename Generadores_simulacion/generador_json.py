import os
import pandas as pd
import json
#from config import rutas # Elimina esta importación

# Obtener la ruta del escritorio
escritorio = os.path.join(os.path.expanduser("~"), "Desktop")

# Ruta del Excel (ahora obtenida del escritorio)
archivo_excel = os.path.join(escritorio, "Datos_Cliente.xlsx")

# Verificar si el archivo Excel existe
if not os.path.exists(archivo_excel):
    print(f"Error: No se encuentra el archivo Excel en la ruta: {archivo_excel}")
    exit()

df = pd.read_excel(archivo_excel)

# Ruta donde vamos a guardar los JSON generados (ahora en el escritorio)
ruta_salida = os.path.join(escritorio, "json_simulacion")
os.makedirs(ruta_salida, exist_ok=True)

# Definir la estructura de documentos y los campos mapeados del Excel
documentos = [
    ("Solicitud Crédito", {
        "No.CREADITO": "No.CREADITO",
        "SOLICITUD": "SOLICITUD",
        "CEDULA": "CEDULA",
        "NOMBRES": "NOMBRES",
        "RECOMPRA O DESEMBOLSO": "Compras de cartera y prepagos",
        "FIRMA ELLECTRONICA": "Firma electrónica (logo y pie)"
    }),
    ("Libranza", {
        "No.CREADITO": "No.CREADITO",
        "NOMBRES": "NOMBRES",
        "CREDITO": "Valor préstamo (crédito)",
        "PAGADURIA": "Pagaduría",
        "CUOTAS": "Cantidad cuotas",
        "VL.CUOTA": "Valor cuota",
        "FIRMA ELLECTRONICA": "Firma electrónica (logo y pie)",
        "AL PIE DE LA FIRMA": "Firma electrónica (logo y pie)"
    }),
    ("Cedula", {
        "CEDULA": "CEDULA",
        "NOMBRES": "NOMBRES",
        "FECHA NACIMIENTO": "Fecha nacimiento"
    }),
    ("Formato conocimiento", {
        "CREDITO": "Monto crédito (Formato conocimiento)",
        "CUOTAS": "Plazo (Formato conocimiento)",
        "FIRMA ELLECTRONICA": "Firma electrónica (logo y pie)",
        "AL PIE DE LA FIRMA": "Firma electrónica (logo y pie)"
    }),
    ("Amortización", {
        "SOLICITUD": "SOLICITUD",
        "CEDULA": "CEDULA",
        "NOMBRES": "NOMBRES",
        "CREDITO": "Valor total a financiar (Amortización)",
        "PAGADURIA": "Entidad pagadora (Amortización)",
        "CUOTAS": "Plazo (Formato conocimiento)",
        "VL.CUOTA": "Valor cuota",
        "E.A": "Tasa E.A. (Amortización)",
        "RECOMPRA O DESEMBOLSO": "Compras de cartera y prepagos",
        "FIRMA ELLECTRONICA": "Firma electrónica (logo y pie)"
    }),
    ("Seguro de vida", {
        "CEDULA": "CEDULA",
        "NOMBRES": "NOMBRES",
        "FIRMA ELLECTRONICA": "Firma electrónica (logo y pie)"
    }),
    ("Fianza", {
        "CEDULA": "CEDULA",
        "NOMBRES": "NOMBRES",
        "FIRMA ELLECTRONICA": "Firma electrónica (logo y pie)",
        "AL PIE DE LA FIRMA": "Firma electrónica (logo y pie)"
    }),
    ("Datacredito", {
        "NOMBRES": "NOMBRES"
    }),
    ("Desprendible Nomina", {
        "CEDULA": "CEDULA",
        "NOMBRES": "NOMBRES",
        "SALARIO": "Valor pensión o salario neto",
        "PAGADURIA": "Pagaduría",
        "FECHA DESPRENDIBLE": "Fecha del desprendible"
    }),
    ("Soportes recompra o soporte desembolso", {
        "CEDULA": "CEDULA",
        "NOMBRES": "NOMBRES",
        "RECOMPRA O DESEMBOLSO": "Valor Total (Soporte desembolso)"
    })
]

# Generar JSON por fila
for idx, row in df.iterrows():
    salida = []

    for doc_nombre, campos_mapeo in documentos:
        campos_final = {}

        for key_destino, columna_excel in campos_mapeo.items():
            # Obtiene el valor de la celda como string, manejando valores NaN
            valor = row.get(columna_excel, "")
            campos_final[key_destino] = str(valor) if pd.notna(valor) else ""


        salida.append({
            "documento": doc_nombre,
            "campos": campos_final
        })

    # Guardar el JSON de esta fila
    nombre_archivo = os.path.join(ruta_salida, f"matriz_datos_extraidos_{idx+1}.json")
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        json.dump(salida, f, indent=4, ensure_ascii=False)

    print(f" Generado JSON: matriz_datos_extraidos_{idx+1}.json")

print(f"Todos los archivos JSON se han generado en: {ruta_salida}")