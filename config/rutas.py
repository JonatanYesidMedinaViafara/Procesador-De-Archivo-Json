import os

# Rutas principales del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__ + "/.."))

CARPETA_JSON = os.path.join(BASE_DIR, "Archivos_json")
CARPETA_NO_JSON = os.path.join(BASE_DIR, "Archivos_no_json")
CARPETA_CON_INCONSISTENCIAS = os.path.join(BASE_DIR, "Archivos_con_inconsistencias")
CARPETA_LOGS = os.path.join(BASE_DIR, "logs")

# Aseguramos que existan las carpetas
for carpeta in [CARPETA_JSON, CARPETA_NO_JSON, CARPETA_CON_INCONSISTENCIAS, CARPETA_LOGS]:
    os.makedirs(carpeta, exist_ok=True)