def main():
    # parametros obligatorios
    
    ancho,alto = tamaño_fractal() # tamaño del fractal
    fractal_inicial = obtener_fractal_inicial(ancho,alto) #diccionario con coord. monticulos y arena en ellos
    nombre_archivo = preguntar_nombre_archivo()
    
    # parametros opcionales
    
    paleta_colores = obtener_paleta_colores()
    tamaño_celda_v,tamaño_celda_h = obtener_tamaño_celda()
    espejado_v,espejado_h = obtener_espejado_fractal()
       
    fractal_con_sandpile = fractal_inicial
    while(True):
        fractal_con_sandpile = sand_piles(fractal_con_sandpile,ancho,alto)
        
        if fractal_con_sandpile == sand_piles(fractal_con_sandpile,ancho,alto): break

    fractal_con_espejado = realizar_espejado(fractal_con_sandpile,ancho,alto,espejado_v,espejado_h)

    with open(nombre_archivo + ".ppm","w") as fractal:
        fractal.write("P3\n")
        fractal.write(str(tamaño_celda_h*ancho*espejado_h)+"\n")
        fractal.write(str(tamaño_celda_v*alto*espejado_v)+"\n")
        fractal.write("255"+"\n")

        for i in range(alto*espejado_v):
            for o in range(tamaño_celda_v):
                for j in range (ancho*espejado_h):
                    for p in range(tamaño_celda_h):
                        fractal.write(paleta_colores[fractal_con_espejado.get((i,j),0)]+"\n")

def tamaño_fractal():
    """ Pregunta al usuario los valores ancho y alto para el tamaño del fractal,
devuelve dichos valores."""

    print("Tamaño del fractal: ")
    
    ancho = input("Ingrese un valor para el ancho del fractal: ")
    alto = input("Ingrese un valor para el alto del fractal: ")
    
    while (not (es_numero_valido(ancho) and es_numero_valido(alto))):
        print("Los valores a ingresar deben ser numeros(mayores que cero), por favor ingrese nuevamente")
        ancho = input("Ingrese un valor para el ancho del fractal: ")
        alto = input("Ingrese un valor para el alto del fractal: ")
    return int(ancho),int(alto)

def es_numero_valido(numero):
    """Recibe una cadena y devuelve un booleano, True si la cadena solo tiene un numero
    con el mismo distinto de 0, y False si la cadena no es un numero o si la misma
    es 0"""
    
    return (numero.isdigit() and int(numero)>0)

def es_coord_valida(fila,columna,ancho,alto):
    """Recibe las coordenas y el tamaño del fractal (ancho y alto), devuelve un booleano que indica si la coordenada
es un valor correcto"""
    coord_fila = ((fila.isdigit() and int(fila)>=0) and int(fila)<int(alto))
    coord_columna = ((columna.isdigit() and int(columna)>=0) and int(columna)<int(ancho))
    return coord_fila and coord_columna

def obtener_fractal_inicial(ancho,alto):
    print("Coordenada de los monticulos y granos de arena en ellos: ")
    fractal = {}
    while(True):
        
        coord_fila = input("Ingrese coordenada de la fila (debe estar entre 0 y {}): ".format(alto-1))
        coord_columna = input("Ingrese coordenada de la columna (debe estar entre 0 y {}): ".format(ancho-1))
        
        while (not es_coord_valida(coord_fila,coord_columna,ancho,alto)):
            print("Por favor, ingrese un valor correcto..")
            coord_fila = input("Ingrese coordenada de la fila (debe estar entre 0 y {}): ".format(alto-1))
            coord_columna = input("Ingrese coordenada de la columna (debe estar entre 0 y {}): ".format(ancho-1))
            
            
        granos_arena = input("Ingrese la cantidad de granos de arena para dicha posicion: ")
        while (not(granos_arena.isdigit() and int(granos_arena)>=0)):
            print("Ingrese un numero mayor o igual a 0")
            granos_arena = input("Ingrese la cantidad de granos de arena para dicha posicion: ")

        
        fractal[(int(coord_fila),int(coord_columna))] = int(granos_arena)
        

        c = input("Desea continuar agregando monticulos? (si = cualquier tecla, no = *)")

        if c == "*": break
    return fractal

def preguntar_nombre_archivo():
    ingresado =  input("Ingrese un nombre para el archivo de salida: (no ingrese el formato): ")
    return ingresado        

def obtener_paleta_colores():
    colores_fractal = { # Colores que tendra cada monticulo (Segun cant. de arena)
    0:"0 0 0",
    1:"255 0 255",
    2:"255 0 0",
    3:"255 255 0"
    }

    ingresado = input("Desea elegir la paleta de colores? (si = cualquier tecla, no = *): ")
    if ingresado == "*":return colores_fractal # Colores por defecto
    
    colores ={          # Colores que el usuario puede elegir (opcional)
     "Negro":"0 0 0",
     "Verde":"0 255 0",
     "Azul":"0 0 255",
     "Rojo":"255 0 0",
     "Violeta":"255 0 255",
     "Celeste":"0 255 255",
     "Naranja":"255 153 0",
     "Rosa":"255 153 204",
     "Amarillo":"255 255 0"
     }

    
    lista_colores = list(colores.keys())

    print("Colores disponibles")
    for i,c in enumerate(lista_colores):
        # i = indice , c = color
        print(i+1,c)

    for granos in range(4):
        c = input("Ingrese el numero del color para cuando el monticulo tenga {} grano/s: ".format(granos))
        while(not(es_numero_valido(c) and int(c)<=8)):
            print("Valor no valido")
            c = input("Ingrese el numero del color para cuando el monticulo tenga {} grano/s: ".format(granos))
        print("El color con {} grano/s sera {}".format(granos,lista_colores[int(c)-1]))
        colores_fractal[granos] = colores[lista_colores[int(c)-1]]
    return colores_fractal

def obtener_tamaño_celda():
    
    tamaño_vertical = 1
    tamaño_horizontal = 1
    
    ingresado = input("Desea elegir el tamaño que tendran los monticulos? (si = cualquier tecla, no = *): ")
    if ingresado == "*":return tamaño_vertical,tamaño_horizontal
    
    tamaño_vertical = input("Ingrese el tamaño vertical de la celda (Seran pixeles): ")
    tamaño_horizontal = input("Ingrese el tamaño horizontal de la celda (Seran pixeles): ")
    
    while (not (es_numero_valido(tamaño_horizontal) and es_numero_valido(tamaño_vertical))):
        print("ERROR. Debe ingresar numeros (mayores que cero)")
        tamaño_vertical = input("Ingrese el tamaño vertical de la celda (Seran pixeles): ")
        tamaño_horizontal = input("Ingrese el tamaño horizontal de la celda (Seran pixeles): ")
        
    return int(tamaño_vertical),int(tamaño_horizontal)

def obtener_espejado_fractal():
    
    espejado_vertical = 1
    espejado_horizontal = 1
    
    ingresado = input("Desea realizarle un espejado al fractal? (si = cualquier tecla, no = *):")
    if ingresado == "*":return espejado_vertical,espejado_horizontal

    print("Tipos de espejado: ")
    print("1. Espejado vertical")
    print("2. Espejado horizontal")
    print("3. Espejado vertical y horizontal")

    tipo_espejado = input("Ingrese el numero de la opcion a elegir (numero entre 1 y 3): ")
    
    while (not (es_numero_valido(tipo_espejado) and int(tipo_espejado)<=3)):
        print("Ingrese un numero entre 1 y 3")
        tipo_espejado = input("Ingrese el numero de la opcion a elegir (numero entre 1 y 3): ")

    if tipo_espejado == "1":
        print("El espejado sera solo vertical")
        espejado_vertical = 2
    elif tipo_espejado == "2":
        print("El espejado sera solo horizontal")
        espejado_horizontal = 2
    else:
        print ("El espejado sera vertical y horizontal")
        espejado_vertical = 2
        espejado_horizontal = 2
        
    return espejado_vertical,espejado_horizontal
 
def sand_piles(fra,ancho,alto):
                            # fra = fractal actual
    frs = {}                # frs = fractal siguiente
    for i,j in fra:
                            # i = fila fra j = columna fra
        d = fra[(i,j)] // 4 # d = valor que distribuye a celdas adyacentes
        
        for pot in range(1,3):
            if d == 0: break
            f = (i+(-1)**pot)
            frs[(f,j)] = frs.get((f,j),0) + d
            if not -1<f<alto:continue
            
            c = (j+(-1)**pot)
            frs[(i,c)] = frs.get((i,c),0) + d
            if not -1<c<ancho:continue
            
        frs[(i,j)] = frs.get((i,j),0) + fra[(i,j)] % 4
        
    return frs   
            
def realizar_espejado(frs,ancho,alto,espejado_v,espejado_h):
    fre = frs
    if espejado_v == 1 and espejado_h == 1: return fre
    elif espejado_v == 1 and espejado_h == 2: # espejado horizontal
        for i in range(alto):
            k = (ancho*2)-1
            for j in range(ancho):
                if not (i,j) in fre:
                    k -=1
                    continue 
                fre[(i,k)] = fre[(i,j)]
                k -= 1
    elif espejado_v == 2 and espejado_h == 1: # espejado vertical
        for j in range(ancho):
            k = (alto*2)-1
            for i in range(alto):
                if not (i,j) in fre:
                    k -=1
                    continue
                fre[(k,j)] = fre[(i,j)]
                k -= 1
    else: # espejado vertical y horizontal
        for i in range(alto):
            k = (ancho*2)-1
            for j in range(ancho):
                if not (i,j) in fre:
                    k -=1
                    continue 
                fre[(i,k)] = fre[(i,j)]
                k -= 1
        for j in range(2*ancho):
            k = (alto*2)-1
            for i in range(alto):
                if not (i,j) in fre:
                    k -=1
                    continue
                fre[(k,j)] = fre[(i,j)]
                k -= 1
        
            
    return fre     

main()
       
        



