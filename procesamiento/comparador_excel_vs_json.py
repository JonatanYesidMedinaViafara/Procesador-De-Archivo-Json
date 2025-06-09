import os
import pandas as pd
import json
import shutil
from config import rutas

# Cargar Excel de datos cliente (reemplaza esta ruta por la ruta real de tu excel maestro)
ruta_excel = os.path.join(os.path.expanduser("~"), "Desktop", "Datos_Cliente.xlsx")
df_excel = pd.read_excel(ruta_excel, dtype=str)

# Creamos carpetas necesarias
ARCHIVO_JSON_NORMALIZADO = rutas.BASE_DIR + "/Archivos_json_normalizados"
CARPETA_NO_ENCONTRADO = rutas.BASE_DIR + "/Archivos_no_excel"
CARPETA_LOG_NO_ENCONTRADO = rutas.BASE_DIR + "/Archivos_no_excel_log"
CARPETA_SI_ENCONTRADO = rutas.BASE_DIR + "/Archivos_si_excel"
os.makedirs(CARPETA_NO_ENCONTRADO, exist_ok=True)
os.makedirs(CARPETA_LOG_NO_ENCONTRADO, exist_ok=True)
os.makedirs(CARPETA_SI_ENCONTRADO, exist_ok=True)

def comparar_vs_excel():
    # todo el código de la comparación aquí
    # Convertimos Excel a diccionario indexado por (CEDULA, No.CREADITO)
    excel_dict = {}
    for _, row in df_excel.iterrows():
        key = (row['CEDULA'], row['No.CREADITO'])
        excel_dict[key] = row.to_dict()

    # Procesamos cada JSON
    for archivo in os.listdir(ARCHIVO_JSON_NORMALIZADO):
        if not archivo.endswith(".json"):
            continue

        ruta_json = os.path.join(ARCHIVO_JSON_NORMALIZADO, archivo)
        with open(ruta_json, 'r', encoding='utf-8') as f:
            data_json = json.load(f)

        # Extraemos los campos clave del json
        # El JSON ya es plano
        json_dict = {
            "CEDULA": str(data_json.get("CEDULA", "")),
            "No.CREADITO": str(data_json.get("No.CREADITO", ""))
        }


        clave_busqueda = (json_dict['CEDULA'], json_dict['No.CREADITO'])

        if clave_busqueda not in excel_dict:
            # JSON no encontrado en excel → lo movemos
            shutil.move(ruta_json, os.path.join(CARPETA_NO_ENCONTRADO, archivo))

            # Generamos log de por qué no está
            log_path = os.path.join(CARPETA_LOG_NO_ENCONTRADO, archivo.replace(".json", ".log"))
            with open(log_path, "w", encoding="utf-8") as log_file:
                log_file.write(f"Archivo: {archivo}\n")
                log_file.write(f"No encontrado en Excel.\n")
                log_file.write(f"Criterios de búsqueda: CEDULA={json_dict['CEDULA']}, No.CREADITO={json_dict['No.CREADITO']}\n")

            print(f"❌ JSON no encontrado en excel → {archivo}")
        else:
            print(f"✅ JSON encontrado: {archivo}")
            # ✅ Si el archivo está en el Excel → lo copiamos a carpeta Archivos_si_excel
            CARPETA_SI_ENCONTRADO = rutas.BASE_DIR + "/Archivos_si_excel"
            os.makedirs(CARPETA_SI_ENCONTRADO, exist_ok=True)

            # Realizamos la copia del archivo
            shutil.copy(ruta_json, os.path.join(CARPETA_SI_ENCONTRADO, archivo))
            # El JSON ya es plano (normalizado)
            json_plano = data_json


            # Traemos la fila de Excel correspondiente
            fila_excel = excel_dict[clave_busqueda]

            # Comparamos todos los campos
            diferencias = []
            for campo_excel, valor_excel in fila_excel.items():
                campo_json = campo_excel  # Los nombres son iguales en tu Excel normalizado
                valor_json = json_plano.get(campo_json, "")

                # Comparamos quitando espacios y ceros a la izquierda (puedes ajustar reglas aquí)
                if str(valor_json).strip() != str(valor_excel).strip():
                    diferencias.append(f"Campo: {campo_excel} → Excel: [{valor_excel}] - JSON: [{valor_json}]")

            # Si hay diferencias generamos log
            if diferencias:
                log_path = os.path.join(rutas.BASE_DIR, "logs", archivo.replace(".json", "_comparacion.log"))
                with open(log_path, "w", encoding="utf-8") as log_file:
                    log_file.write(f"Archivo: {archivo}\n")
                    log_file.write("Inconsistencias encontradas:\n")
                    for diff in diferencias:
                        log_file.write(diff + "\n")
                print(f"❌ Diferencias encontradas en {archivo} (ver log)")
            else:
                print(f"✅ {archivo} validado completamente, campos OK")
