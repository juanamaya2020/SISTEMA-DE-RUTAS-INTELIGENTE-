import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score




# ============================================================
# RUTA DEL DATASET
# ============================================================


RUTA_DATASET = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "datos",
    "dataset.csv"
)

print("========================================")
print("ENTRENAMIENTO DEL MODELO")
print("========================================")
print()

print("Leyendo dataset:")
print(RUTA_DATASET)
print()


# ============================================================
# CARGAR DATASET
# ============================================================

datos = pd.read_csv(

    RUTA_DATASET,
    sep=",",
    encoding="utf-8-sig"
)


# ============================================================
# MOSTRAR COLUMNAS DETECTADAS
# ============================================================

print("Columnas detectadas:")
print(datos.columns.tolist())
print()


# ============================================================
# LIMPIAR NOMBRES DE COLUMNAS
# ============================================================

datos.columns = (
    datos.columns
    .str.strip()
    .str.replace("\ufeff", "", regex=False)
)


# ============================================================
# VERIFICAR COLUMNAS NECESARIAS
# ============================================================

columnas_necesarias = [
    "origen",
    "destino",
    "distancia_km",
    "hora",
    "dia_semana",
    "pasajeros",
    "transbordos",
    "clima",
    "congestion",
    "tiempo_min"
]

faltantes = [
    columna
    for columna in columnas_necesarias
    if columna not in datos.columns
]

if faltantes:

    print("ERROR: faltan las siguientes columnas:")
    print(faltantes)
    print()

    print("Las columnas encontradas fueron:")
    print(datos.columns.tolist())

    print()
    print("Revisa que el archivo dataset.csv")
    print("tenga las columnas separadas correctamente.")

    raise SystemExit


# ============================================================
# CONVERTIR CLIMA A NUMEROS
# ============================================================

datos["clima"] = datos["clima"].map({
    "Normal": 0,
    "Nublado": 1,
    "Lluvia": 2
})


# ============================================================
# VARIABLES DE ENTRADA
# ============================================================

X = datos[
    [
        "distancia_km",
        "hora",
        "dia_semana",
        "pasajeros",
        "transbordos",
        "clima",
        "congestion"
    ]
]


# ============================================================
# VARIABLE OBJETIVO
# ============================================================

y = datos["tiempo_min"]


# ============================================================
# DIVIDIR DATOS
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# ============================================================
# CREAR MODELO
# ============================================================

modelo = DecisionTreeRegressor(
    max_depth=6,
    random_state=42
)


# ============================================================
# ENTRENAR
# ============================================================

print("Entrenando modelo...")
print()

modelo.fit(X_train, y_train)


# ============================================================
# PREDICCIONES
# ============================================================

predicciones = modelo.predict(X_test)


# ============================================================
# EVALUACION
# ============================================================

mae = mean_absolute_error(
    y_test,
    predicciones
)

mse = mean_squared_error(
    y_test,
    predicciones
)

r2 = r2_score(
    y_test,
    predicciones
)


print("========================================")
print("RESULTADOS DEL MODELO")
print("========================================")
print()

print(f"MAE: {mae:.2f}")
print(f"MSE: {mse:.2f}")
print(f"R²: {r2:.2f}")

print()


# ============================================================
# PRUEBA DE PREDICCION
# ============================================================

nueva_ruta = pd.DataFrame({

    "distancia_km": [17.5],

    "hora": [7],

    "dia_semana": [0],

    "pasajeros": [3000],

    "transbordos": [1],

    "clima": [0],

    "congestion": [8]

})


tiempo_estimado = modelo.predict(
    nueva_ruta
)


print("========================================")
print("PREDICCION DE NUEVA RUTA")
print("========================================")
print()

print("Distancia: 17.5 km")
print("Hora: 7:00")
print("Pasajeros: 3000")
print("Transbordos: 1")
print("Congestion: 8/10")

print()

print(
    f"Tiempo estimado: "
    f"{tiempo_estimado[0]:.2f} minutos"
)

print()


# ============================================================
# GUARDAR MODELO
# ============================================================

RUTA_MODELO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "modelo_tiempo.pkl"
)


joblib.dump(
    modelo,
    RUTA_MODELO
)


print("========================================")
print("MODELO GUARDADO CORRECTAMENTE")
print("========================================")
print()

print(RUTA_MODELO)