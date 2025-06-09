import os
import json
from helpers.lector_json import cargar_json
from validadores.validador_interno import ValidadorInterno
from config import rutas

# Creamos la carpeta si no existe
os.makedirs(os.path.join(rutas.BASE_DIR, "Archivos_json_normalizados"), exist_ok=True)

def consolidar_campos(data):
    campos_claves = ["CEDULA", "NOMBRES", "No.CREADITO", "SOLICITUD"]
    consolidado = {}

    for campo in campos_claves:
        valores = set()

        for documento in data:
            campos = documento.get("campos", {})
            valor = campos.get(campo)
            if valor is not None:
                valores.add(valor)

        if len(valores) == 1:
            consolidado[campo] = list(valores)[0]
        else:
            # Aquí ya no debería ocurrir porque son JSON ya validados
            consolidado[campo] = list(valores)

    return consolidado

def normalizar_archivos():
    for archivo in os.listdir(rutas.CARPETA_JSON):
        ruta_archivo = os.path.join(rutas.CARPETA_JSON, archivo)

        if archivo.lower().endswith('.json'):
            try:
                data = cargar_json(ruta_archivo)
                validador = ValidadorInterno(data)
                inconsistencias = validador.validar()

                if inconsistencias:
                    print(f"⚠ El archivo {archivo} tiene inconsistencias y no debería estar aquí.")
                else:
                    consolidado = consolidar_campos(data)

                    ruta_salida = os.path.join(rutas.BASE_DIR, "Archivos_json_normalizados", archivo)
                    with open(ruta_salida, 'w', encoding='utf-8') as f:
                        json.dump(consolidado, f, indent=4, ensure_ascii=False)

                    print(f"✅ Archivo normalizado generado: {archivo}")

            except Exception as e:
                print(f"⚠ Error al procesar {archivo}: {e}")
