import os
import shutil
from helpers.lector_json import cargar_json
from helpers.logger import escribir_log_individual
from helpers.validador_estructura import es_estructura_valida
from validadores.validador_interno import ValidadorInterno
from validadores.validador_coherencia_global import ValidadorCoherenciaGlobal
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
    archivo_actual = os.path.basename(path_archivo)

    try:
        data = cargar_json(path_archivo)
    except Exception as e:
        print(f"❌ Error cargando {archivo_actual} como JSON: {e}")
        mover_a_no_json(path_archivo, archivo_actual)
        return

    if not es_estructura_valida(data):
        print(f"❌ Estructura inválida → {archivo_actual}. Movido a 'Archivos_con_inconsistencias'")
        mover_a_inconsistentes(path_archivo, archivo_actual)
        return

    nombre_base = os.path.splitext(archivo_actual)[0]
    partes = nombre_base.split("_")
    if len(partes) != 3:
        print(f"❌ Nombre mal formado → {archivo_actual}. Movido a 'Archivos_con_inconsistencias'")
        mover_a_inconsistentes(path_archivo, archivo_actual)
        return

    numero_cargue, credito_nombre, cedula_nombre = partes

    cedulas = set()
    creditos = set()

    for documento in data:
        campos = documento.get("data_extraida", {})
        if "numero_documento" in campos:
            cedulas.add(str(campos["numero_documento"]))
        if "numero_credito" in campos:
            creditos.add(str(campos["numero_credito"]))

    if len(cedulas) != 1 or len(creditos) != 1:
        print(f"❌ CEDULA o numero_credito ausente o inconsistentes → {archivo_actual}")
        print(f"   → Cedulas encontradas: {cedulas}")
        print(f"   → Creditos encontrados: {creditos}")
        mover_a_inconsistentes(path_archivo, archivo_actual)
        return

    cedula_json = cedulas.pop()
    credito_json = creditos.pop()

    if cedula_json != cedula_nombre or credito_json != credito_nombre:
        print(f"❌ CEDULA/numero_credito no coincide con nombre → {archivo_actual}")
        print(f"   → En nombre: CEDULA={cedula_nombre}, CREDITO={credito_nombre}")
        print(f"   → En JSON:   CEDULA={cedula_json}, CREDITO={credito_json}")
        mover_a_inconsistentes(path_archivo, archivo_actual)
        return

    validador = ValidadorInterno(data)
    inconsistencias = validador.validar()

    mensajes_log = []
    if inconsistencias:
        mensajes_log.append(f"❌ Inconsistencias encontradas en {archivo_actual}:")
        for campo, valores in inconsistencias.items():
            mensajes_log.append(f"  → Campo '{campo}' tiene múltiples valores: {valores}")
        mover_a_inconsistentes(path_archivo, archivo_actual)
    else:
        mensajes_log.append(f"✅ {archivo_actual} validado correctamente (estructura + coherencia interna).")

    validador_global = ValidadorCoherenciaGlobal(data)
    inconsistencias_globales = validador_global.validar()

    if inconsistencias_globales:
        mensajes_log.append(f"❌ Inconsistencias globales detectadas en {archivo_actual}:")
        for campo, valores in inconsistencias_globales.items():
            mensajes_log.append(f"  → Campo '{campo}' tiene múltiples valores: {valores}")
        validador_global.exportar_excel_reporte(
            archivo_actual,
            inconsistencias_globales,
            rutas.CARPETA_CON_INCONSISTENCIAS
        )
        mover_a_inconsistentes(path_archivo, archivo_actual)

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
                    print(f"⚠ Error inesperado al procesar el archivo {archivo}: {e}")
            else:
                mover_a_no_json(ruta, archivo)
