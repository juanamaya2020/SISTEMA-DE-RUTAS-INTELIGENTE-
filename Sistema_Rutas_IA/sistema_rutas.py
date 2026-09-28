import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import math


# SISTEMA INTELIGENTE DE BÚSQUEDA DE RUTAS 



ESTACIONES = {

    "Portal Norte": {
        "posicion": (80, 80)
    },

    "Toberín": {
        "posicion": (140, 130)
    },

    "Calle 142": {
        "posicion": (200, 180)
    },

    "Prado": {
        "posicion": (260, 230)
    },

    "Calle 127": {
        "posicion": (320, 280)
    },

    "Calle 100": {
        "posicion": (380, 330)
    },

    "La Castellana": {
        "posicion": (440, 380)
    },

    "NQS Calle 75": {
        "posicion": (500, 430)
    },

    "7 de Agosto": {
        "posicion": (560, 480)
    },

    "Universidad Nacional": {
        "posicion": (620, 530)
    },

    "Av. Eldorado": {
        "posicion": (680, 580)
    },

    "Ricaurte": {
        "posicion": (740, 630)
    },

    "Comuneros": {
        "posicion": (800, 680)
    },

    "General Santander": {
        "posicion": (860, 730)
    },

    "Perdomo": {
        "posicion": (920, 780)
    },

    "Portal Sur": {
        "posicion": (980, 830)
    },


    # RUTAS ALTERNATIVAS HIPOTÉTICAS

    "Calle 26": {
        "posicion": (620, 420)
    },

    "Quinta Paredes": {
        "posicion": (560, 350)
    },

    "Av. Jiménez": {
        "posicion": (700, 470)
    },

    "Las Aguas": {
        "posicion": (780, 420)
    },

    "Portal Américas": {
        "posicion": (850, 350)
    }
}


# ........................................................
# 2. BASE DE CONOCIMIENTO
# .......................................................


CONEXIONES = [

    # Ruta principal

    ("Portal Norte", "Toberín", 1),
    ("Toberín", "Calle 142", 1),
    ("Calle 142", "Prado", 1),
    ("Prado", "Calle 127", 1),
    ("Calle 127", "Calle 100", 1),
    ("Calle 100", "La Castellana", 1),
    ("La Castellana", "NQS Calle 75", 1),
    ("NQS Calle 75", "7 de Agosto", 1),
    ("7 de Agosto", "Universidad Nacional", 1),
    ("Universidad Nacional", "Av. Eldorado", 1),
    ("Av. Eldorado", "Ricaurte", 1),
    ("Ricaurte", "Comuneros", 1),
    ("Comuneros", "General Santander", 1),
    ("General Santander", "Perdomo", 1),
    ("Perdomo", "Portal Sur", 1),

    # ............................................
    # Rutas alternativas
    # .............................................

    ("Calle 100", "Calle 26", 3),
    ("Calle 26", "Av. Eldorado", 2),

    ("La Castellana", "Quinta Paredes", 3),
    ("Quinta Paredes", "Av. Jiménez", 3),
    ("Av. Jiménez", "Ricaurte", 2),

    ("Av. Jiménez", "Las Aguas", 2),
    ("Las Aguas", "Portal Américas", 3),
    ("Portal Américas", "Av. Eldorado", 4)
]



# 3. CONSTRUCCIÓN DEL GRAFO


def construir_grafo():

    grafo = {}

    # los nodos

    for estacion in ESTACIONES:

        grafo[estacion] = []


    # conexiones

    for origen, destino, costo in CONEXIONES:

        # Conexión de ida

        grafo[origen].append(
            (destino, costo)
        )

        # Conexión de regreso, en este caso o modelo las conexiones las o considero como bidireccionales.

        grafo[destino].append(
            (origen, costo)
        )

    return grafo


GRAFO = construir_grafo()



# 4. SISTEMA BASADO EN REGLAS

# REGLA 1, si existe una conexión entre A y B, ENTONCES B es alcanzable desde A.
# REGLA 2, Si B es alcanzable desde A, ENTONCES B puede ser utilizado como siguiente estado de búsqueda.

def aplicar_reglas(estacion):

    destinos_validos = []

    # Consultamos los hechos relacionados con la estación actual.

    for destino, costo in GRAFO[estacion]:

        # Regla:
        #
        # Si existe conexión(A,B)
        # entonces B puede ser alcanzado desde A.

        destinos_validos.append(
            (destino, costo)
        )

    return destinos_validos


# .....................................
# 5. FUNCIÓN HEURÍSTICA
# ..............................
#
# A* utiliza:
#
#               f(n) = g(n) + h(n)
#
# g(n) = costo acumulado
#
# h(n) = estimación del costo restante
#
# ........................................

def heuristica(estacion_actual, destino):

    x1, y1 = ESTACIONES[
        estacion_actual
    ]["posicion"]

    x2, y2 = ESTACIONES[
        destino
    ]["posicion"]


    # Distancia euclidiana

    distancia = math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )

    return distancia


# 6. ALGORITMO A*


# la idea es que  algoritmo busque una ruta de menor costo.#


def buscar_ruta(origen, destino):

    # .....................
    # Validación
    # ............

    if origen not in GRAFO:

        return None, None

    if destino not in GRAFO:

        return None, None


    # ..............................
    # Caso en que origen y destino son iguales
    #..........................................

    if origen == destino:

        return [origen], 0


    # ..............................
    # Cola de prioridad
    # ...............................

    frontera = []

    contador = 0


    # f(n), contador, estación

    heapq.heappush(
        frontera,
        (
            0,
            contador,
            origen
        )
    )


    # ...................................................
    # Costos acumulados
    # ...................................................

    costos = {

        origen: 0

    }


   
    # Permite reconstruir la ruta al final.


    padres = {

        origen: None

    }


   
    # Estados visitados


    visitados = set()


    # BÚSQUEDA


    while frontera:

        _, _, actual = heapq.heappop(
            frontera
        )



        # Si llegamos al destino
      

        if actual == destino:

            ruta = []

            nodo = actual


            while nodo is not None:

                ruta.append(
                    nodo
                )

                nodo = padres[nodo]


            # La ruta se construye de atrás, hacia adelante, por eso la invertimos.

            ruta.reverse()


            return (
                ruta,
                costos[destino]
            )



        # Evitar procesar un estado dos veces


        if actual in visitados:

            continue


        visitados.add(
            actual
        )


        # aquie podemos aplicar las reglas


        vecinos = aplicar_reglas(
            actual
        )


        # Explorar vecinos

        for vecino, costo in vecinos:

            nuevo_costo = (
                costos[actual] +
                costo
            )


            # aquie podemos ver si encontramos una ruta, más económica hacia el vecino

            if (
                vecino not in costos
                or
                nuevo_costo < costos[vecino]
            ):

                costos[vecino] = (
                    nuevo_costo
                )


                padres[vecino] = (
                    actual
                )



                # Heurística
    

                h = heuristica(
                    vecino,
                    destino
                )


                # ...............................
                # Función A*
                #
                # f(n) = g(n) + h(n)
                # ....................................

                f = (
                    nuevo_costo +
                    h
                )


                contador += 1


                heapq.heappush(
                    frontera,
                    (
                        f,
                        contador,
                        vecino
                    )
                )



    # No se encontró una ruta

    return None, None


# .....................................
# 7. INTERFAZ GRÁFICA
# ...................................

class Aplicacion:


    def __init__(self, ventana):

        self.ventana = ventana


        # ----------------------------------------------------
        # CONFIGURACIÓN DE LA VENTANA
        # ----------------------------------------------------

        self.ventana.title(
            "Sistema Inteligente de Rutas"
        )


        self.ventana.geometry(
            "1250x850"
        )


        self.ventana.minsize(
            1100,
            750
        )


        self.ventana.configure(
            bg="#F2F2F2"
        )

        # TÍTULO


        titulo = tk.Label(

            ventana,

            text=(
                "SISTEMA INTELIGENTE "
                "DE BÚSQUEDA DE RUTAS"
            ),

            font=(
                "Arial",
                20,
                "bold"
            ),

            bg="#F2F2F2"

        )

        titulo.pack(
            pady=15
        )


  
        # PANEL DE SELECCIÓN
     

        panel = tk.Frame(

            ventana,

            bg="#FFFFFF",

            bd=1,

            relief="solid"

        )

        panel.pack(

            padx=15,

            pady=5,

            fill="x"

        )


        # ORIGEN
  

        tk.Label(

            panel,

            text="¿Dónde estás?",

            font=(
                "Arial",
                11,
                "bold"
            ),

            bg="#FFFFFF"

        ).grid(

            row=0,

            column=0,

            padx=10,

            pady=15

        )


        self.origen = ttk.Combobox(

            panel,

            values=list(
                ESTACIONES.keys()
            ),

            state="readonly",

            width=27

        )


        self.origen.grid(

            row=0,

            column=1,

            padx=10

        )


      
        # DESTINO
 

        tk.Label(

            panel,

            text="¿A dónde quieres llegar?",

            font=(
                "Arial",
                11,
                "bold"
            ),

            bg="#FFFFFF"

        ).grid(

            row=0,

            column=2,

            padx=10

        )


        self.destino = ttk.Combobox(

            panel,

            values=list(
                ESTACIONES.keys()
            ),

            state="readonly",

            width=27

        )


        self.destino.grid(

            row=0,

            column=3,

            padx=10

        )


        # BOTÓN
     

        boton = tk.Button(

            panel,

            text="BUSCAR RUTA",

            command=self.calcular_ruta,

            font=(
                "Arial",
                11,
                "bold"
            ),

            padx=25,

            pady=8,

            cursor="hand2"

        )


        boton.grid(

            row=0,

            column=4,

            padx=15

        )


        # CONTENEDOR PRINCIPAL
    

        contenido = tk.Frame(

            ventana,

            bg="#F2F2F2"

        )


        contenido.pack(

            fill="both",

            expand=True,

            padx=15,

            pady=10

        )

        # MAPA
      

        mapa_frame = tk.Frame(

            contenido,

            bg="#FFFFFF",

            bd=1,

            relief="solid"

        )


        mapa_frame.pack(

            side="left",

            fill="both",

            expand=True

        )


        self.canvas = tk.Canvas(

            mapa_frame,

            bg="#FFFFFF",

            highlightthickness=0

        )


        self.canvas.pack(

            fill="both",

            expand=True,

            padx=5,

            pady=5

        )


       
        # PANEL RESULTADO
    

        resultado_panel = tk.Frame(

            contenido,

            bg="#FFFFFF",

            width=300,

            bd=1,

            relief="solid"

        )


        resultado_panel.pack(

            side="right",

            fill="y",

            padx=(10, 0)

        )


        resultado_panel.pack_propagate(
            False
        )


  
        # TÍTULO RESULTADO


        tk.Label(

            resultado_panel,

            text="RESULTADO",

            font=(
                "Arial",
                16,
                "bold"
            ),

            bg="#FFFFFF"

        ).pack(

            pady=15

        )


        # TEXTO RESULTADO
     

        self.resultado = tk.Text(

            resultado_panel,

            font=(
                "Arial",
                10
            ),

            wrap="word",

            bd=0,

            bg="#FFFFFF"

        )


        self.resultado.pack(

            fill="both",

            expand=True,

            padx=15,

            pady=10

        )



        # INFORMACIÓN INICIAL


        self.resultado.insert(

            tk.END,

            "Seleccione un punto de origen\n"

            "y un punto de destino.\n\n"

            "Después presione:\n\n"

            "BUSCAR RUTA\n\n"

            "El sistema utilizará el\n"

            "algoritmo A* para buscar\n"

            "una ruta de menor costo."

        )


        # ----------------------------------------------------
        # EVENTO PARA REDIBUJAR EL MAPA
        # ----------------------------------------------------

        self.canvas.bind(

            "<Configure>",

            self.al_mostrar_mapa

        )


        # DIBUJAR MAPA


        self.dibujar_mapa()


    # .................................................................
    # TRANSFORMAR COORDENADAS
    # ...............................................................
    #
    # en este pedaso la función es la modificación principal.
    #
    # Calcula automáticamente la escala necesaria para que
    # TODAS las estaciones entren en el Canvas.
    #
    # ..................................................................

    def transformar_coordenadas(
        self,
        x,
        y
    ):


        # Obtener tamaño actual del Canvas


        ancho = self.canvas.winfo_width()

        alto = self.canvas.winfo_height()


        # Si todavía no tiene tamaño real, utilizar valores de respaldo.

        if ancho < 100:

            ancho = 900

        if alto < 100:

            alto = 600



        # Obtener todas las coordenadas

        coordenadas = [

            datos["posicion"]

            for datos
            in ESTACIONES.values()

        ]


        min_x = min(
            x for x, y in coordenadas
        )

        max_x = max(
            x for x, y in coordenadas
        )

        min_y = min(
            y for x, y in coordenadas
        )

        max_y = max(
            y for x, y in coordenadas
        )


    
        # Márgenes
  

        margen = 70


        espacio_ancho = (
            ancho - margen * 2
        )

        espacio_alto = (
            alto - margen * 2
        )


    
        # Calcula la escala
     

        escala_x = (
            espacio_ancho /
            (max_x - min_x)
        )

        escala_y = (
            espacio_alto /
            (max_y - min_y)
        )


        # aqui poemos Utilizamos la menor escala para garantizar, que todo el mapa entre.

        escala = min(
            escala_x,
            escala_y
        )


        # con esto evitaremos escalas exageradas

        escala = min(
            escala,
            1.0
        )


        # Calcularemos dimensiones reales
 

        ancho_mapa = (
            max_x - min_x
        ) * escala

        alto_mapa = (
            max_y - min_y
        ) * escala



        # Centrar el mapa
   

        inicio_x = (
            (ancho - ancho_mapa) / 2
        )

        inicio_y = (
            (alto - alto_mapa) / 2
        )


      
        # Transformar coordenadas
   

        nuevo_x = (

            inicio_x +

            (x - min_x) * escala

        )


        nuevo_y = (

            inicio_y +

            (y - min_y) * escala

        )


        return (
            nuevo_x,
            nuevo_y
        )


    # ========================================================
    # EVENTO DEL CANVAS
    # ========================================================

    def al_mostrar_mapa(
        self,
        evento=None
    ):

        self.dibujar_mapa()


    # ========================================================
    # DIBUJAR MAPA
    # ========================================================

    def dibujar_mapa(
        self,
        ruta=None
    ):

        self.canvas.delete(
            "all"
        )


        # DIBUJAR CONEXIONES
 

        for origen, destino, costo in CONEXIONES:


            # Coordenadas originales

            x1, y1 = ESTACIONES[
                origen
            ]["posicion"]

            x2, y2 = ESTACIONES[
                destino
            ]["posicion"]


            # Transformar coordenadas

            x1, y1 = self.transformar_coordenadas(
                x1,
                y1
            )

            x2, y2 = self.transformar_coordenadas(
                x2,
                y2
            )


            # Determnar si pertenece a la ruta


            pertenece = False


            if ruta:

                for i in range(
                    len(ruta) - 1
                ):

                    estacion_a = ruta[i]

                    estacion_b = ruta[i + 1]


                    if (

                        (
                            estacion_a == origen
                            and
                            estacion_b == destino
                        )

                        or

                        (
                            estacion_a == destino
                            and
                            estacion_b == origen
                        )

                    ):

                        pertenece = True

                        break


    
            # para eestilo de conexión
  

            if pertenece:

                color = "#E53935"

                ancho = 5

            else:

                color = "#C5C5C5"

                ancho = 2



            # Dibujar línea
     

            self.canvas.create_line(

                x1,
                y1,

                x2,
                y2,

                fill=color,

                width=ancho

            )


        # DIBUJAR ESTACIONES


        for estacion, datos in ESTACIONES.items():


            # Coordenadas originales

            x, y = datos[
                "posicion"
            ]


            # Transformar coordenadas

            x, y = self.transformar_coordenadas(
                x,
                y
            )


            # Color predeterminado
     

            color = "#1976D2"


            # ------------------------------------------------
            # Origen
            # ------------------------------------------------

            if (
                self.origen.get()
                == estacion
            ):

                color = "#2E7D32"


            # Destino
  

            if (
                self.destino.get()
                == estacion
            ):

                color = "#C62828"


            # Estación perteneciente a la ruta
      

            if (

                ruta

                and

                estacion in ruta

            ):

                color = "#FF9800"


     
            # Dibujar punto
         

            self.canvas.create_oval(

                x - 7,
                y - 7,

                x + 7,
                y + 7,

                fill=color,

                outline="#333333"

            )


            # Nombre
  

            self.canvas.create_text(

                x + 10,

                y,

                text=estacion,

                anchor="w",

                font=(
                    "Arial",
                    8
                ),

                fill="#222222"

            )


        # LEYENDA


        self.canvas.create_text(

            15,

            15,

            text="● Origen    ● Destino    ● Ruta",

            anchor="nw",

            font=(
                "Arial",
                9,
                "bold"
            ),

            fill="#333333"

        )


    # ========================================================
    # CALCULAR RUTA
    # ========================================================

    def calcular_ruta(
        self
    ):


        # ----------------------------------------------------
        # Obtener selección
        # ----------------------------------------------------

        origen = self.origen.get()

        destino = self.destino.get()


        # ----------------------------------------------------
        # Validación
        # ----------------------------------------------------

        if not origen:

            messagebox.showwarning(

                "Origen",

                "Seleccione el punto de origen."

            )

            return


        if not destino:

            messagebox.showwarning(

                "Destino",

                "Seleccione el punto de destino."

            )

            return


        if origen == destino:

            messagebox.showwarning(

                "Ruta",

                "El origen y destino son iguales."

            )

            return


        # ----------------------------------------------------
        # Ejecutar A*
        # ----------------------------------------------------

        ruta, costo = buscar_ruta(

            origen,

            destino

        )


        # ----------------------------------------------------
        # No existe ruta
        # ----------------------------------------------------

        if ruta is None:

            self.resultado.delete(

                "1.0",

                tk.END

            )


            self.resultado.insert(

                tk.END,

                "NO SE ENCONTRÓ UNA RUTA\n\n"

                "El sistema no encontró una conexión "
                "entre los puntos seleccionados."

            )


            self.dibujar_mapa()

            return


        # ----------------------------------------------------
        # Mostrar resultado
        # ----------------------------------------------------

        self.resultado.delete(

            "1.0",

            tk.END

        )


        self.resultado.insert(

            tk.END,

            "RUTA ENCONTRADA\n"

            "========================\n\n"

        )


        self.resultado.insert(

            tk.END,

            f"ORIGEN:\n"
            f"{origen}\n\n"

        )


        self.resultado.insert(

            tk.END,

            f"DESTINO:\n"
            f"{destino}\n\n"

        )


        self.resultado.insert(

            tk.END,

            "RUTA RECOMENDADA:\n\n"

        )


        # ----------------------------------------------------
        # Mostrar estaciones
        # ----------------------------------------------------

        for i, estacion in enumerate(ruta):

            self.resultado.insert(

                tk.END,

                f"{i + 1}. {estacion}\n"

            )


            # Flecha entre estaciones

            if i < len(ruta) - 1:

                self.resultado.insert(

                    tk.END,

                    "       ↓\n"

                )


        # ----------------------------------------------------
        # Información adicional
        # ----------------------------------------------------

        self.resultado.insert(

            tk.END,

            "\n========================\n"

        )


        self.resultado.insert(

            tk.END,

            f"ESTACIONES: {len(ruta)}\n"

        )


        self.resultado.insert(

            tk.END,

            f"TRANSICIONES: {len(ruta) - 1}\n"

        )


        self.resultado.insert(

            tk.END,

            f"COSTO ESTIMADO: {costo}\n\n"

        )


        # ------------------------------
        # Información del algoritm
        # -----------------------------

        self.resultado.insert(

            tk.END,

            "ALGORITMO:\n"

            "A* (A-Star)\n\n"

        )


        self.resultado.insert(

            tk.END,

            "FUNCIÓN DE EVALUACIÓN:\n"

            "f(n) = g(n) + h(n)\n\n"

        )


        self.resultado.insert(

            tk.END,

            "g(n): costo acumulado\n"

            "h(n): estimación restante\n"

            "f(n): costo total estimado\n"

        )


        # ................................................
        # Dibujar ruta
        # ----------------------------------------------------

        self.dibujar_mapa(

            ruta

        )


# ...................................................................
# 8. EJECUTAR APLICACIÓN
# ....................................................................

if __name__ == "__main__":

    ventana = tk.Tk()

    aplicacion = Aplicacion(
        ventana
    )

    ventana.mainloop()
