from procesamiento import procesador_archivos, normalizador_json, comparador_excel_vs_json

if __name__ == "__main__":
    print("🔎 FASE 1: Validando archivos internos...")
    procesador_archivos.procesar_carpeta()

    # print("\n📦 FASE 1.5: Normalizando archivos válidos...")
    # normalizador_json.normalizar_archivos()

    # print("\n🔍 FASE 2: Comparando contra Excel maestro...")
    # comparador_excel_vs_json.comparar_vs_excel()
