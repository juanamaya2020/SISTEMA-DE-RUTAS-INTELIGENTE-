import os
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# ============================================================
# 1. UBICACIÓN DEL DATASET
# ============================================================

RUTA_DATASET = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "datos",
    "dataset.csv"
)


# ============================================================
# 2. CARGAR DATASET
# ============================================================

datos = pd.read_csv(
    RUTA_DATASET,
    sep=";",
    decimal=",",
    encoding="utf-8-sig"
)


# ============================================================
# 3. LIMPIAR COLUMNAS
# ============================================================

datos.columns = (
    datos.columns
    .astype(str)
    .str.strip()
    .str.replace("\ufeff", "", regex=False)
    .str.lower()
)

print("\nCOLUMNAS DEL DATASET:")
for columna in datos.columns:
    print(repr(columna))


# ============================================================
# 4. BUSCAR COLUMNA CLIMA
# ============================================================

columna_clima = None

for columna in datos.columns:
    if columna.strip().lower() == "clima":
        columna_clima = columna
        break


if columna_clima is None:

    print("\nNO SE ENCONTRO LA COLUMNA CLIMA.")

    print("\nColumnas disponibles:")
    print(datos.columns.tolist())

    raise SystemExit


print("\nColumna clima encontrada correctamente:")
print(repr(columna_clima))


# ============================================================
# 5. CONVERTIR CLIMA
# ============================================================

datos[columna_clima] = datos[columna_clima].astype(str).str.strip()

datos[columna_clima] = datos[columna_clima].map({
    "Normal": 0,
    "Nublado": 1,
    "Lluvia": 2
})


# ============================================================
# 6. VARIABLES PARA K-MEANS
# ============================================================

variables = [
    "distancia_km",
    "hora",
    "pasajeros",
    "transbordos",
    columna_clima,
    "congestion"
]

# Convertir todas las variables a valores numéricos
for columna in variables:
    datos[columna] = pd.to_numeric(
        datos[columna],
        errors="coerce"
    )

# ============================================================
# 7. CREAR X
# ============================================================

X = datos[variables].copy()


# ============================================================
# 8. ELIMINAR DATOS VACIOS
# ============================================================

X = X.dropna()

print("\nRegistros utilizados para K-Means:")
print(len(X))


# ============================================================
# 9. NORMALIZAR
# ============================================================

escalador = StandardScaler()

X_escalado = escalador.fit_transform(X)


# ============================================================
# 10. K-MEANS
# ============================================================

modelo = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)


# ============================================================
# 11. ENTRENAMIENTO
# ============================================================

grupos = modelo.fit_predict(X_escalado)


# ============================================================
# 12. GUARDAR GRUPOS
# ============================================================

datos.loc[X.index, "grupo"] = grupos

datos["grupo"] = datos["grupo"].astype("Int64")


# ============================================================
# 13. RESULTADOS
# ============================================================

print("\n========================================")
print("AGRUPAMIENTO K-MEANS")
print("========================================")

print("\nCantidad de registros por grupo:")

print(
    datos["grupo"]
    .value_counts()
    .sort_index()
)


# ============================================================
# 14. PROMEDIOS
# ============================================================

print("\nCaracterísticas promedio de cada grupo:")

resumen = datos.groupby("grupo")[variables].mean()

print(resumen)


# ============================================================
# 15. EJEMPLOS
# ============================================================

print("\nPrimeros registros clasificados:")

print(
    datos[
        [
            "origen",
            "destino",
            "distancia_km",
            "hora",
            "pasajeros",
            "congestion",
            "grupo"
        ]
    ].head(10)
)


# ============================================================
# 16. GUARDAR RESULTADO
# ============================================================

RUTA_RESULTADO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "dataset_agrupado.csv"
)

datos.to_csv(
    RUTA_RESULTADO,
    index=False,
    encoding="utf-8-sig"
)


print("\n========================================")
print("PROCESO TERMINADO CORRECTAMENTE")
print("========================================")

print("\nArchivo generado:")
print(RUTA_RESULTADO)