import os
from config import rutas

def escribir_log_individual(nombre_archivo_json, mensajes):
    nombre_log = nombre_archivo_json + ".log"
    path_log = os.path.join(rutas.CARPETA_LOGS, nombre_log)

    with open(path_log, "w", encoding="utf-8") as log_file:
        for mensaje in mensajes:
            log_file.write(mensaje + "\n")
