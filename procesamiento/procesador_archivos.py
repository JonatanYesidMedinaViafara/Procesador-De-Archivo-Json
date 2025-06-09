import os
import shutil
from helpers.lector_json import cargar_json
from helpers.logger import escribir_log_individual
from validadores.validador_interno import ValidadorInterno
from config import rutas

def mover_a_inconsistentes(ruta_archivo, archivo_actual):
    destino = os.path.join(rutas.CARPETA_CON_INCONSISTENCIAS, archivo_actual)
    shutil.move(ruta_archivo, destino)
    print(f"⚠ Archivo con inconsistencias movido a 'Archivos_con_inconsistencias': {archivo_actual}")

def mover_a_no_json(ruta_archivo, archivo_actual):
    destino = os.path.join(rutas.CARPETA_NO_JSON, archivo_actual)
    shutil.move(ruta_archivo, destino)
    print(f"📦 Archivo no json movido a 'Archivos_no_json': {archivo_actual}")

def procesar_archivo(path_archivo):
    data = cargar_json(path_archivo)
    validador = ValidadorInterno(data)
    inconsistencias = validador.validar()

    archivo_actual = os.path.basename(path_archivo)
    mensajes_log = []

    if inconsistencias:
        mensajes_log.append(f"❌ Inconsistencias encontradas en {archivo_actual}:")
        for campo, valores in inconsistencias.items():
            mensajes_log.append(f"  → Campo '{campo}' tiene múltiples valores: {valores}")
        mover_a_inconsistentes(path_archivo, archivo_actual)
    else:
        mensajes_log.append(f"✅ {archivo_actual} validado correctamente (coherencia interna).")

    escribir_log_individual(archivo_actual, mensajes_log)

    for m in mensajes_log:
        print(m)

def procesar_carpeta():
    for archivo in os.listdir(rutas.CARPETA_JSON):
        ruta = os.path.join(rutas.CARPETA_JSON, archivo)

        if os.path.isfile(ruta):
            if archivo.lower().endswith('.json'):
                try:
                    procesar_archivo(ruta)
                except Exception as e:
                    print(f"⚠ Error al procesar el archivo {archivo}: {e}")
            else:
                mover_a_no_json(ruta, archivo)
