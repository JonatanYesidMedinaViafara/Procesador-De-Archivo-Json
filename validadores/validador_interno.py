class ValidadorInterno:
    def __init__(self, data):
        self.data = data
        self.campos_claves = ["CEDULA", "NOMBRES", "No.CREADITO", "SOLICITUD"]

    def extraer_valores(self):
        valores = {campo: set() for campo in self.campos_claves}

        for documento in self.data:
            campos = documento.get("campos", {})
            for campo in self.campos_claves:
                valor = campos.get(campo)
                if valor is not None:
                    valores[campo].add(str(valor))

        return valores

    def validar(self):
        inconsistencias = {}
        valores = self.extraer_valores()

        for campo, conjunto in valores.items():
            if len(conjunto) > 1:
                inconsistencias[campo] = list(conjunto)
        return inconsistencias
