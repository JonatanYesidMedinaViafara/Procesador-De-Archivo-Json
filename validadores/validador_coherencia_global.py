import pandas as pd
import os

class ValidadorCoherenciaGlobal:
    def __init__(self, data):
        self.data = data

    def validar(self):
        valores_por_campo = {}

        for documento in self.data:
            campos = documento.get("data_extraida", {})
            for campo, valor in campos.items():
                valor = str(valor).strip()
                if campo not in valores_por_campo:
                    valores_por_campo[campo] = set()
                valores_por_campo[campo].add(valor)

        inconsistencias = {
            campo: list(valores)
            for campo, valores in valores_por_campo.items()
            if len(valores) > 1
        }

        return inconsistencias

    def exportar_excel_reporte(self, nombre_archivo, inconsistencias, carpeta_destino):
        ruta = os.path.join(carpeta_destino, nombre_archivo.replace(".json", "_inconsistencias.xlsx"))
        df = pd.DataFrame([
            {"Campo": campo, "Valores distintos": ", ".join(valores)}
            for campo, valores in inconsistencias.items()
        ])
        df.to_excel(ruta, index=False)
