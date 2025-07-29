import os
import pandas as pd
import json
import shutil
from config import rutas

# Ruta al Excel maestro
ruta_excel = os.path.join(os.path.expanduser("~"), "Desktop", "Datos_Cliente.xlsx")
df_excel = pd.read_excel(ruta_excel, dtype=str)

# Carpetas involucradas
ARCHIVO_JSON_NORMALIZADO = os.path.join(rutas.BASE_DIR, "Archivos_json_normalizados")
CARPETA_NO_ENCONTRADO = os.path.join(rutas.BASE_DIR, "Archivos_no_excel")
CARPETA_LOG_NO_ENCONTRADO = os.path.join(rutas.BASE_DIR, "Archivos_no_excel_log")
CARPETA_SI_ENCONTRADO = os.path.join(rutas.BASE_DIR, "Archivos_si_excel")
CARPETA_LOG_INCONSISTENCIAS = os.path.join(rutas.BASE_DIR, "logs")

# Aseguramos la existencia de carpetas
os.makedirs(CARPETA_NO_ENCONTRADO, exist_ok=True)
os.makedirs(CARPETA_LOG_NO_ENCONTRADO, exist_ok=True)
os.makedirs(CARPETA_SI_ENCONTRADO, exist_ok=True)
os.makedirs(CARPETA_LOG_INCONSISTENCIAS, exist_ok=True)

def comparar_vs_excel():
    # Convertimos el Excel a un diccionario indexado por (CEDULA, No.CREADITO)
    excel_dict = {
        (row['CEDULA'], row['No.CREADITO']): row.to_dict()
        for _, row in df_excel.iterrows()
    }

    # Recorremos cada JSON normalizado
    for archivo in os.listdir(ARCHIVO_JSON_NORMALIZADO):
        if not archivo.endswith(".json"):
            continue

        ruta_json = os.path.join(ARCHIVO_JSON_NORMALIZADO, archivo)
        with open(ruta_json, 'r', encoding='utf-8') as f:
            data_json = json.load(f)

        # Extraemos cédula y número de crédito
        cedula = str(data_json.get("CEDULA", "")).strip()
        credito = str(data_json.get("No.CREADITO", "")).strip()
        clave = (cedula, credito)

        if clave not in excel_dict:
            # Si no se encuentra, se mueve y genera log
            shutil.move(ruta_json, os.path.join(CARPETA_NO_ENCONTRADO, archivo))

            log_path = os.path.join(CARPETA_LOG_NO_ENCONTRADO, archivo.replace(".json", ".log"))
            with open(log_path, "w", encoding="utf-8") as log:
                log.write(f"Archivo: {archivo}\n")
                log.write("No encontrado en Excel.\n")
                log.write(f"Criterios de búsqueda: CEDULA={cedula}, No.CREADITO={credito}\n")

            print(f"❌ JSON no encontrado en Excel → {archivo}")
            continue

        # Si se encuentra → copiar a carpeta de éxito
        shutil.copy(ruta_json, os.path.join(CARPETA_SI_ENCONTRADO, archivo))
        print(f"✅ JSON encontrado: {archivo}")

        fila_excel = excel_dict[clave]
        diferencias = []

        # Comparamos cada campo
        for campo_excel, valor_excel in fila_excel.items():
            valor_json = str(data_json.get(campo_excel, "")).strip()
            valor_excel = str(valor_excel).strip()

            if valor_json != valor_excel:
                diferencias.append(f"Campo: {campo_excel} → Excel: [{valor_excel}] - JSON: [{valor_json}]")

        if diferencias:
            log_path = os.path.join(CARPETA_LOG_INCONSISTENCIAS, archivo.replace(".json", "_comparacion.log"))
            with open(log_path, "w", encoding="utf-8") as log:
                log.write(f"Archivo: {archivo}\n")
                log.write("Inconsistencias encontradas:\n")
                for diff in diferencias:
                    log.write(diff + "\n")
            print(f"❌ Diferencias encontradas en {archivo} (ver log)")
        else:
            print(f"✅ {archivo} validado completamente, campos OK")

