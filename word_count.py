#
# Escriba la función load_input que recive como parámetro un folder y retorna
# una lista de tuplas donde el primer elemento de cada tupla es el nombre del
# archivo y el segundo es una línea del archivo. La función convierte a tuplas
# todas las lineas de cada uno de los archivos. La función es genérica y debe
# leer todos los archivos de folder entregado como parámetro.
#
# Por ejemplo:
#   [
#     ('text0'.txt', 'Analytics is the discovery, inter ...'),
#     ('text0'.txt', 'in data. Especially valuable in ar...').
#     ...
#     ('text2.txt'. 'hypotheses.')
#   ]
#
import glob
import fileinput

def load_input(input_directory):
    sequence = []
    filenames = glob.glob(input_directory + "/*") #glob permite leer contenido de una carpeta, /* para que me aparezca todo lo que esta en el archivo
    with fileinput.input(files=filenames) as f:         #el fileinput lo vuelve iterador
        for line in f:          #para devolver una a una las lineas de los archivos uno a uno
            sequence.append((fileinput.filename(), line))
    return sequence  #genere lista de tuplas con las lineas de los archivos


#
# Escriba una función llamada maper que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). En este caso,
# la clave es cada palabra y el valor es 1, puesto que se está realizando un
# conteo.
#
#   [
#     ('Analytics', 1),
#     ('is', 1),
#     ...
#   ]
#
def mapper(sequence):               #defino la función mapper que depende de sequence
    new_sequence = []               
    for _, text in sequence:         #asigno nombre de archivo y texto, _ coge el ultimo reusultado
        words = text.split()            #separa las palabras
        for word in words:
            word = word.replace(",", "")
            word = word.replace(".", "")
            word = word.lower()
            new_sequence.append((word, 1))  #agrega los elementos al final de la lista
    return new_sequence
#esto nos hace el MAp, duplas en lista con valor


#
# Escriba la función shuffle_and_sort que recibe la lista de tuplas entregada
# por el mapper, y retorna una lista con el mismo contenido ordenado por la
# clave.
#
#   [
#     ('Analytics', 1),
#     ('Analytics', 1),
#     ...
#   ]
#La unica tarea de esta funcion es ordenar la secuencia
def shuffle_and_sort(sequence):
    sorted_sequence = sorted(sequence, key=lambda x: x[0]) #lambda es funcion anonima que recibe x y devuelve x[0]
    return sorted_sequence

#
# Escriba la función reducer, la cual recibe el resultado de shuffle_and_sort y
# reduce los valores asociados a cada clave sumandolos. Como resultado, por
# ejemplo, la reducción indica cuantas veces aparece la palabra analytics en el
# texto.
#
def reducer(sequence):
    diccionario = {}
    for key, value in sequence:
        if key not in diccionario.keys():  #si no le agrego, no me permite asignar valores porque no existe ninguna key
            diccionario[key] = []   #a la key le agrego una lista vacía como valor
        diccionario[key].append(value)   #luego a esa key, al valor (que antes era vacio) agrego value

    new_sequence = []
    for key, value in diccionario.items():
        tupla = (key, sum(value))
        new_sequence.append(tupla)
    return new_sequence


#
# Escriba la función create_ouptput_directory que recibe un nombre de directorio
# y lo crea. Si el directorio existe, la función falla.
#
import os.path   #permite hacer operaciones en archivos

def create_output_directory(output_directory):
    if os.path.exists(output_directory):   #para ver si el archivo existe
        raise FileExistsError(f"The directory '{output_directory}' already exists")
    os.makedirs(output_directory)


#
# Escriba la función save_output, la cual almacena en un archivo de texto llamado
# part-00000 el resultado del reducer. El archivo debe ser guardado en el
# directorio entregado como parámetro, y que se creo en el paso anterior.
# Adicionalmente, el archivo debe contener una tupla por línea, donde el primer
# elemento es la clave y el segundo el valor. Los elementos de la tupla están
# separados por un tabulador.
#
def save_output(output_directory, sequence):
    with open(output_directory + "/part-00000", "w") as file:
        for key, value in sequence:
            file.write(f"{key}\t{value}\n")


#
# La siguiente función crea un archivo llamado _SUCCESS en el directorio
# entregado como parámetro.
#
def create_marker(output_directory):
    with open(output_directory + "/_SUCCES", "w") as file:   #este archivo vacio es para decir que quedo bien
        file.write("")

#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def job(input_directory, output_directory):
    sequence = load_input(input_directory)
    sequence = mapper(sequence)
    sequence = shuffle_and_sort(sequence)
    sequence = reducer(sequence)
    create_output_directory(output_directory)
    save_output(output_directory, sequence)
    create_marker(output_directory)


if __name__ == "__main__":   #para que solo se llame job cuando llamo el archivo word_count
    job(
        "input",
        "output",
    )
