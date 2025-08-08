import requests
import csv
import time
from PIL import Image

from Obra import Obra
from libreria_pillow import guardar_imagen_desde_url
from funciones import *

class MetroArt:
    """ Clase principal MetroArt que tiene las funcionalidades del 
        sistema de catálogo de la colección de arte.
    """    
    
    def __init__(self):
        """ Método constructor de la clase MetroArt.
        Inicializa el museo con un nombre y listas vacías para obras y departamentos.
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
        """        
        self.nombre_del_museo = "Museo metropolitano de Arte"
        self.obras = [] 
        self.departamentos = []
        self.nacionalidades = []
        self.obras_por_departamento = {}
        self.obras_por_nacionalidad = {}

    def leer_api(self,url):
        """ Metodo para leer la API del museo metropolitano de arte.
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
            url (str): URL a leer.
        Retorna:
            Los datos obtenidos de la respuesta de la lectura para luego manipularlos y utilizarlos
        """
        while True:
            print('.',end="")
            try:
                respuesta = requests.get(url)
                respuesta.raise_for_status()
                if respuesta.status_code == 200:
                    datos = respuesta.json()                    
                    break
            except requests.exceptions.RequestException as e:
                if e.response.status_code == 404:
                    datos = None
                    break
                #print(e)
                time.sleep(1.5)
                continue
        return datos 
        
    
    def cargar_datos_API(self):
        """ Metodo para cargar los datos de la API del museo metropolitano de arte.
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
        
            Carga los datos iniciales desde la API, en este caso los departamentos, la función
            se ejecuta pero no tiene un valor de retorno
        """        
        
        print(f'\n---------- Cargando desde la API ----------\n')        
        #Cargo los departamentos
        url = "https://collectionapi.metmuseum.org/public/collection/v1/departments"
        datos = self.leer_api(url)
        
        if datos is None:
            print("La API no permitió leer los departamentos")
        
        else:
            for departamento in datos['departments']:
                self.departamentos.append(departamento)
        
        print(f'\n---------- Carga finalizada. ----------\n')
    
    def cargar_datos_csv(self, archivo):
        """ Metodo para cargar las nacionalidades del archivo CSV.
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
            archivo (str): Ruta del archivo CSV a cargar.
            
            Carga los datos iniciales desde el CSV, en este caso las nacionalidades, la función
            se ejecuta pero no tiene un valor de retorno
        """
        print(f'\n---------- Cargando desde CSV ----------\n')
        with open(archivo, mode='r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            
            next(lector_csv)  # Omite la cabecera del CSV
            
            filas = list(lector_csv)
            for fila in filas:
                nueva_nacionalidad = fila[0]
                self.nacionalidades.append(nueva_nacionalidad)
        
        #print(self.nacionalidades)
        
        print(f"Se cargaron {len(self.nacionalidades)} nacionalidades.")
        
        print(f'\n---------- Carga desde CSV finalizada. ----------\n')
    
    def mostrar_imagen(self, url,titulo):
        """ Metodo para mostrar una imagen desde una URL.
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
            url (str): URL de la imagen a mostrar.
            
            Si consigue un link se ejecuta, almacena la foto y la muestra
        """
        if url == '':
            print("La obra no tiene imagen.")
        else:
            eleccion_mostrar_imagen = input('''
                ¿Desea ver la imagen de la obra en una nueva ventana? Ingrese "y" si lo desea o "n" en caso contrario:''')
            if eleccion_mostrar_imagen.lower() == "y":
                # Nombre deseado para el archivo (sin extensión, ya que se determinará automáticamente) 
                nombre_archivo_destino = f"imagenes/{titulo}" 
                # Llamar a la función para guardar la imagen 
                nombre_archivo_destino=guardar_imagen_desde_url(url, nombre_archivo_destino) 
                img = Image.open(nombre_archivo_destino) 
                img.show()
    
    def submenu_obras_por_departamento(self,nombre_del_departamento,ids_de_obras=[]):
        """ Metodo para mostrar las obras de un departamento.
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
            nombre_del_departamento (str): Nombre del departamento.
            ids_de_obras (list): IDs de las obras a mostrar.
            
            Si se le pasa una lista con las obras esta recorrerá la lista e imprimirá el menu
            con las obras dando la opcion de ver mas detalles de esta.
            Si no se le pasa ninguna lista, buscará la lista de ids en las obras almacenadas usando el nombre del
            departamento y mostrará luego el mismo menu dado que se llama recursivamente
        """
        if ids_de_obras == []:
            ids_de_obras = self.obras_por_departamento[nombre_del_departamento]
            self.submenu_obras_por_departamento(nombre_del_departamento, ids_de_obras)
            
        while True:
                print(" ")
                print(f"---------- Departamento {nombre_del_departamento} ----------")
                print(" ")
                for obra in self.obras:
                    if obra.numero in ids_de_obras:
                        print(obra.mostrar_para_listado())
                print(" ")
                numero_de_la_obra_a_mostrar = input("Ingrese el numero de una obra para mostrar sus detalles o el numero 0 para salir: ")
                while not es_numero(numero_de_la_obra_a_mostrar):
                    print(" ")
                    print("Intente de nuevo.")
                    print(" ")
                    numero_de_la_obra_a_mostrar = input("Ingrese el numero de una obra para mostrar sus detalles o el numero 0 para salir: ")
                
                # Si decide salir 
                if numero_de_la_obra_a_mostrar == '0': 
                    break
                
                #Verifico que el id pertenece a una obra. Si no sale busco su elección
                obra_encontrada = False
                obra_a_mostrar = " "
                for obra in self.obras:
                    if obra.numero == int(numero_de_la_obra_a_mostrar):
                        obra_encontrada = True
                        obra_a_mostrar = obra
                        break
                    
                # Si no seleccionó un departamento valido de la lista
                if obra_encontrada == False:
                    print('')
                    print("Número de obra no existente.")
                    continue
                
                print(obra_a_mostrar.mostrar_detalles_completos())
                
                # Para mostrar la imagen
                api_url = obra_a_mostrar.imagen_de_la_obra
                titulo = obra_a_mostrar.titulo.replace(" ", "_")  # Reemplazo espacios por guiones bajos para el nombre del archivo
                    
                self.mostrar_imagen(api_url,titulo)
            
    def busqueda_por_departamento(self):
        """ Metodo para la funcionalidad de busqueda por departamento.
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
        
            Imprime la lista de departamentos para que el usuario seleccione uno eligiendo un numero
            y lleva al submenu para saber mas detalles de estas.
            Si el numero de departamento es valido busca si tiene la información guardada, 
            si no consulta a la API y guarda y muestra la obra
        """        

        while True:
            # Imprimo los departamentos y guardo la elección del usuario
            print("---------- Busqueda por departamento ----------")
            print('')
            for departamento in self.departamentos:
                print(f"Departamento #{departamento['departmentId']}: {departamento['displayName']}")
            print('')
            numero_del_departamento_seleccionado = input("Ingrese el numero del departamento que desea consultar o el numero 0 para salir: ")
            while not es_numero(numero_del_departamento_seleccionado):
                print(" ")
                print("Intente de nuevo.")
                print(" ")
                numero_del_departamento_seleccionado = input("Ingrese el numero del departamento que desea consultar o el numero 0 para salir: ")
                
            # Si decide salir 
            if numero_del_departamento_seleccionado == "0": 
                print(" ")
                break
            
            # Si no sale busco su elección
            departamento_encontrado = False
            nombre_del_departamento = " "
            for departamento in self.departamentos:
                if departamento['departmentId'] == int(numero_del_departamento_seleccionado):
                    departamento_encontrado = True
                    nombre_del_departamento = departamento['displayName']
                    break
            
            # Si no seleccionó un departamento valido de la lista
            if departamento_encontrado == False:
                print('')
                print("Número de departamento invalido")
                continue
            print(' ')
            print(f"Buscando obras por {nombre_del_departamento} ")
            print(' ')
            # Si es valido busco las obras
            if len(self.obras_por_departamento)>0:
                # Verifico si ya se buscó en algun momento
                encontrado = self.obras_por_departamento.get(nombre_del_departamento,-1)
                
                # {
                    # Artes modernas: [1,2,3]
                # }
                
                # Si esta en el diccionario se procede a mostrar las obras USAR FUNCION
                if encontrado != -1:
                    
                    # lista es la que contiene las obras
                    ids_de_obras = self.obras_por_departamento[nombre_del_departamento]
 
                    self.submenu_obras_por_departamento(nombre_del_departamento, ids_de_obras)
                    
                    continue #Si la consiguió no hace buscar en la API, vuelve al bucle
                
            print("No almacenadas, se procede a buscar en la API")
            print(" ")    
            # Busco las obras por ese departamento en la API
            url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?departmentId={numero_del_departamento_seleccionado}&q=cat"
            
            datos = self.leer_api(url)
            
            ids_de_obras = datos['objectIDs']
            
            print("Recuperando obras desde la API. Espere por favor...") 
            print("")
            if ids_de_obras == None:
                print("No existen resultados para el nombre de autor ingresado")
                print(" ")
                continue
            
            self.obras_por_departamento[nombre_del_departamento] = ids_de_obras # Guardo los ids de obras del departamento
            print(f"Filtrando de {len(ids_de_obras)} resultados.")
            print('')
            print("Revisando obras:")
            for numero_de_obra in ids_de_obras:
                print(f"    Obra numero {numero_de_obra}") 
                url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{numero_de_obra}"
                obra_respuesta = self.leer_api(url)
                
                if obra_respuesta is None:
                    print("Obra no válida en la API. No almacenada.")
                    continue
                
                numero = obra_respuesta['objectID']
                
                titulo = obra_respuesta['title'],
                if titulo == " " or titulo == "":
                    titulo = "No especificado"
                if type(titulo) == tuple:
                    titulo = titulo[0]
                
                nombre_del_autor = obra_respuesta['artistDisplayName'],
                if type(nombre_del_autor) == str:
                    nombre_del_autor = nombre_del_autor.replace("(","").replace(")","").replace(",","")
                if nombre_del_autor == " " or nombre_del_autor == "":
                    nombre_del_autor = "No especificado"
                if type(nombre_del_autor) == tuple:   # ("nombre ejemplo", ) Me salia esto en la API
                    nombre_del_autor = nombre_del_autor[0]
                
                nacionalidad_del_autor = obra_respuesta['artistNationality'],
                if nacionalidad_del_autor == " " or nacionalidad_del_autor == "":
                    nacionalidad_del_autor = "No especificada"
                if type(nacionalidad_del_autor) == tuple:
                    nacionalidad_del_autor = nacionalidad_del_autor[0]
                
                fecha_de_nacimiento = obra_respuesta['artistBeginDate'],
                if fecha_de_nacimiento == " " or fecha_de_nacimiento == "":
                    fecha_de_nacimiento = "No especificada"
                if type(fecha_de_nacimiento) == tuple:
                    fecha_de_nacimiento = fecha_de_nacimiento[0]
                
                fecha_de_muerte = obra_respuesta['artistEndDate'],
                if fecha_de_muerte == " " or fecha_de_muerte == "":
                    fecha_de_muerte = "No especificada"
                if type(fecha_de_muerte) == tuple:
                    fecha_de_muerte = fecha_de_muerte[0]
                
                tipo = obra_respuesta['classification'],
                if tipo == " " or tipo == "":
                    tipo = "No especificado"
                if type(tipo) == tuple:
                    tipo = tipo[0]
                
                año_de_creación = obra_respuesta['objectDate'],
                if año_de_creación == " " or año_de_creación == "":
                    año_de_creación = "No especificado"
                if type(año_de_creación) == tuple:
                    año_de_creación = año_de_creación[0]
                
                imagen_de_la_obra = obra_respuesta['primaryImage']
                if type(imagen_de_la_obra) == tuple:
                    imagen_de_la_obra = imagen_de_la_obra[0]
                    
                nueva_obra = Obra(
                    numero,
                    titulo,
                    nombre_del_autor,
                    nacionalidad_del_autor,
                    fecha_de_nacimiento,
                    fecha_de_muerte,
                    tipo,
                    año_de_creación,
                    imagen_de_la_obra,
                    )
                
                #Verifico que no este guardada
                guardada = False
                for obra in self.obras:
                    if obra.numero == nueva_obra.numero:
                        guardada = True
                        
                if not guardada:
                    self.obras.append(nueva_obra)
                    
            self.submenu_obras_por_departamento(nombre_del_departamento, ids_de_obras)
    
    def submenu_obras_por_nacionalidad(self,nombre_de_la_nacionalidad,ids_de_obras=[]):
        """ Metodo para mostrar las obras filtrando por nacionalidad del autor.
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
            nombre_de_la_nacionalidad (str): Nombre del nacionalidad.
            ids_de_obras (list): IDs de las obras a mostrar.
            
            Si se le pasa una lista con las obras esta recorrerá la lista e imprimirá el menu
            con las obras dando la opcion de ver mas detalles de esta.
            Si no se le pasa ninguna lista, buscará la lista de ids en las obras almacenadas usando el nombre del
            nacionalidad y mostrará luego el mismo menu dado que se llama recursivamente
        """
        if ids_de_obras == []:
            ids_de_obras = self.obras_por_nacionalidad[nombre_de_la_nacionalidad]
            self.submenu_obras_por_nacionalidad(nombre_de_la_nacionalidad, ids_de_obras)
            
        while True:
                print(" ")
                print(f"---------- Nacionalidad {nombre_de_la_nacionalidad} ----------")
                print(" ")
                for obra in self.obras:
                    if obra.numero in ids_de_obras:
                        print(obra.mostrar_para_listado())
                print(" ")
                numero_de_la_obra_a_mostrar = input("Ingrese el numero una obra para mostrar sus detalles o el numero 0 para salir: ")
                while not es_numero(numero_de_la_obra_a_mostrar):
                    print(" ")
                    print("Intente de nuevo.")
                    print(" ")
                    numero_de_la_obra_a_mostrar = input("Ingrese el numero una obra para mostrar sus detalles o el numero 0 para salir: ")
                
                # Si decide salir 
                if numero_de_la_obra_a_mostrar == '0': 
                    break
                
                #Verifico que el id pertenece a una obra. Si no sale busco su elección
                obra_encontrada = False
                obra_a_mostrar = " "
                for obra in self.obras:
                    if obra.numero == int(numero_de_la_obra_a_mostrar):
                        obra_encontrada = True
                        obra_a_mostrar = obra
                        break
                    
                # Si no seleccionó un nacionalidad valido de la lista
                if obra_encontrada == False:
                    print('')
                    print("Número de obra no existente.")
                    continue
                
                print(obra_a_mostrar.mostrar_detalles_completos())
                
                # Para mostrar la imagen
                api_url = obra.imagen_de_la_obra
                titulo = obra.titulo.replace(" ", "_")  # Reemplazo espacios por guiones bajos para el nombre del archivo
                    
                self.mostrar_imagen(api_url,titulo)
                            
    def busqueda_por_nacionalidad_del_autor(self):
        """ Metodo para la funcionalidad de busqueda por nacionalidad.
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
        
            Imprime la lista de nacionalidades para que el usuario seleccione una eligiendo un numero
            y lleva al submenu para saber mas detalles de estas.
            Si el numero de nacionalidad es valido busca si tiene la información guardada, 
            si no consulta a la API y guarda y muestra la obra
        """        
        while True:
            # Imprimo los nacionalidads y guardo la elección del usuario
            print("---------- Busqueda por nacionalidad ----------")
            print('')
            for i in range(len(self.nacionalidades)):
                print(f"{i+1} {self.nacionalidades[i]}")
            print('')
            numero_de_la_nacionalidad_seleccionado = input("Ingrese el numero de la nacionalidad que desea consultar o el numero 0 para salir: ")
            while not es_numero(numero_de_la_nacionalidad_seleccionado) or int(numero_de_la_nacionalidad_seleccionado) not in range(0,len(self.nacionalidades)+1):
                print(" ")
                print("Intente de nuevo.")
                print(" ")
                numero_de_la_nacionalidad_seleccionado = input("Ingrese el numero de la nacionalidad que desea consultar o el numero 0 para salir: ")
                
            # Si decide salir 
            if numero_de_la_nacionalidad_seleccionado == "0": 
                break
            
            nombre_de_la_nacionalidad = self.nacionalidades[int(numero_de_la_nacionalidad_seleccionado)-1]
            print(f"Buscando obras por {nombre_de_la_nacionalidad} ")
            print(' ')
            # Si es valido busco las obras
            if len(self.obras_por_nacionalidad)>0:
                # Verifico si ya se buscó en algun momento
                encontrado = self.obras_por_nacionalidad.get(nombre_de_la_nacionalidad,-1)
                
                # Si esta en el diccionario se procede a mostrar las obras USAR FUNCION
                if encontrado != -1:
                    print("Entré")
                    print(nombre_de_la_nacionalidad)
                    print(self.obras_por_departamento[nombre_de_la_nacionalidad])

                    # lista es la que contiene las obras
                    ids_de_obras = self.obras_por_nacionalidad[nombre_de_la_nacionalidad]

                    self.submenu_obras_por_nacionalidad(nombre_de_la_nacionalidad, ids_de_obras)
                    
                    continue #Si la consiguió no hace buscar en la API, vuelve al bucle
                
            print("No almacenadas, se procede a buscar en la API")
            print(" ")    
            
            # Busco las obras por ese nacionalidad en la API
            url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?artistOrCulture=true&q={nombre_de_la_nacionalidad}"
            
            datos = self.leer_api(url)
            
            ids_de_obras = datos['objectIDs']
            
            print("Recuperando obras desde la API. Espere por favor...") 
            print("")
            if ids_de_obras == None:
                print("No existen resultados para el nombre de autor ingresado")
                print(" ")
                continue
                 
            # Las guardo en el nacionalidad
            self.obras_por_nacionalidad[nombre_de_la_nacionalidad] = ids_de_obras
            print(f"Filtrando de {len(ids_de_obras)} resultados.")
            print('')
            print("Revisando obras:")
            for numero_de_obra in ids_de_obras: 
                print(f"    Obra numero {numero_de_obra}") 
                url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{numero_de_obra}"
                
                obra_respuesta = self.leer_api(url)
                
                if obra_respuesta is None:
                    print("Obra no válida en la API. No almacenada.")
                    continue
                
                if obra_respuesta['artistNationality'] == nombre_de_la_nacionalidad:    
                    numero = obra_respuesta['objectID']

                    titulo = obra_respuesta['title'],
                    if titulo == " " or titulo == "":
                        titulo = "No especificado"
                    if type(titulo) == tuple:
                        titulo = titulo[0]

                    nombre_del_autor = obra_respuesta['artistDisplayName'],
                    print(nombre_del_autor)
                    print(type(nombre_del_autor))
                    if type(nombre_del_autor) == str:
                        nombre_del_autor = nombre_del_autor.replace("(","").replace(")","").replace(",","")
                    if nombre_del_autor == " " or nombre_del_autor == "":
                        nombre_del_autor = "No especificado"
                    if type(nombre_del_autor) == tuple:
                        nombre_del_autor = nombre_del_autor[0]

                    nacionalidad_del_autor = obra_respuesta['artistNationality'],
                    if nacionalidad_del_autor == " " or nacionalidad_del_autor == "":
                        nacionalidad_del_autor = "No especificada"
                    if type(nacionalidad_del_autor) == tuple:
                        nacionalidad_del_autor = nacionalidad_del_autor[0]

                    fecha_de_nacimiento = obra_respuesta['artistBeginDate'],
                    if fecha_de_nacimiento == " " or fecha_de_nacimiento == "":
                        fecha_de_nacimiento = "No especificada"
                    if type(fecha_de_nacimiento) == tuple:
                        fecha_de_nacimiento = fecha_de_nacimiento[0]

                    fecha_de_muerte = obra_respuesta['artistEndDate'],
                    if fecha_de_muerte == " " or fecha_de_muerte == "":
                        fecha_de_muerte = "No especificada"
                    if type(fecha_de_muerte) == tuple:
                        fecha_de_muerte = fecha_de_muerte[0]

                    tipo = obra_respuesta['classification'],
                    if tipo == " " or tipo == "":
                        tipo = "No especificado"
                    if type(tipo) == tuple:
                        tipo = tipo[0]

                    año_de_creación = obra_respuesta['objectDate'],
                    if año_de_creación == " " or año_de_creación == "":
                        año_de_creación = "No especificado"
                    if type(año_de_creación) == tuple:
                        año_de_creación = año_de_creación[0]

                    imagen_de_la_obra = obra_respuesta['primaryImage']
                    if type(imagen_de_la_obra) == tuple:
                        imagen_de_la_obra = imagen_de_la_obra[0]

                    nueva_obra = Obra(
                        numero,
                        titulo,
                        nombre_del_autor,
                        nacionalidad_del_autor,
                        fecha_de_nacimiento,
                        fecha_de_muerte,
                        tipo,
                        año_de_creación,
                        imagen_de_la_obra,
                        )
                        #Verifico que no este guardada
                    guardada = False
                    for obra in self.obras:
                        if obra.numero == nueva_obra.numero:
                            guardada = True

                    if not guardada:
                        self.obras.append(nueva_obra)

            self.submenu_obras_por_nacionalidad(nombre_de_la_nacionalidad, ids_de_obras)
    
    def submenu_obras_por_nombre(self,nombre_autor,ids_de_obras):
        """ Metodo para mostrar las obras de un nombre buscado.
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
            nombre_autor (str): Nombre del autor a buscar.
            ids_de_obras (list): IDs de las obras a mostrar.
            
            Recorre la lista de obras que se le envian e imprimirá el menu
            con las obras dando la opcion de ver mas detalles de esta.
        """    
        if len(ids_de_obras)!=0:
            while True:
                    print(" ")
                    print(f"---------- Nombre del autor: {nombre_autor} ----------")
                    print(" ")
                    for obra in self.obras:
                        if obra.numero in ids_de_obras:
                            print(obra.mostrar_para_listado())
                    print(" ")
                    numero_de_la_obra_a_mostrar = input("Ingrese el numero una obra para mostrar sus detalles o el numero 0 para salir: ")
                    while not es_numero(numero_de_la_obra_a_mostrar):
                        print(" ")
                        print("Intente de nuevo.")
                        print(" ")
                        numero_de_la_obra_a_mostrar = input("Ingrese el numero una obra para mostrar sus detalles o el numero 0 para salir: ")

                    # Si decide salir 
                    if numero_de_la_obra_a_mostrar == '0': 
                        break
                    
                    #Verifico que el id pertenece a una obra. Si no sale busco su elección
                    obra_encontrada = False
                    obra_a_mostrar = " "
                    for obra in self.obras:
                        if obra.numero == int(numero_de_la_obra_a_mostrar):
                            obra_encontrada = True
                            obra_a_mostrar = obra
                            break
                        
                    # Si no seleccionó un nombre valido de la lista
                    if obra_encontrada == False:
                        print('')
                        print("Número de obra no existente.")
                        continue
                    
                    print(obra_a_mostrar.mostrar_detalles_completos())

                    # Para mostrar la imagen
                    api_url = obra_a_mostrar.imagen_de_la_obra
                    titulo = obra_a_mostrar.titulo.replace(" ", "_")  # Reemplazo espacios por guiones bajos para el nombre del archivo

                    self.mostrar_imagen(api_url,titulo)    
        else:
            print("No existen resultados para el nombre de autor ingresado")

    def busqueda_por_nombre_del_autor(self):
        """ Metodo para la funcionalidad de busqueda por nombre del autor.
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
        
            Permite ingresar un nombre del autor para que el programa busque a las obras correspondientes
            por coincidencia parcial con el nombre.
            
            Si no hay ninguna coincidencia indica al usuario
        """        
        while True:
            # Imprimo los  y guardo la elección del usuario
            print(" ")
            print("---------- Busqueda por autor ----------")
            print('')
            nombre_autor = input("Ingrese el nombre y apellido del autor que desea consultar con un solo espacio (el separador) o el numero 0 para salir: ")
            while not es_nombre(nombre_autor) and nombre_autor !="0":
                print(" ")
                print("Intente de nuevo.")
                print(" ")
                nombre_autor = input("Ingrese el nombre y apellido del autor que desea consultar con un solo espacio (el separador) o el numero 0 para salir: ")
                
            # Si decide salir 
            if nombre_autor == "0": 
                break
            
            print(' ')
            print(f"Buscando obras por {nombre_autor} ")
            print(' ')
            
            # Busco las obras por ese nombre de autor en la API
            url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?artistOrCulture=true&q={nombre_autor}"
            
            datos = self.leer_api(url)
            ids_de_obras = datos['objectIDs']        
            
            print("Recuperando obras desde la API. Espere por favor...") 
            print(" ")
            if ids_de_obras == None:
                print("No existen resultados para el nombre de autor ingresado")
                print(" ")
                continue
            
            print(f"Filtrando de {len(ids_de_obras)} resultados.")
            print('')     
            print("Revisando obras:")
            for numero_de_obra in ids_de_obras: 
                print(f"    Obra numero {numero_de_obra}") 
                url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{numero_de_obra}"
                
                obra_respuesta = self.leer_api(url)
                
                if obra_respuesta is None:
                    print("Obra no válida en la API. No almacenada.")
                    continue
                
                numero = obra_respuesta['objectID']
                
                titulo = obra_respuesta['title'],
                if titulo == " " or titulo == "":
                    titulo = "No especificado"
                if type(titulo) == tuple:
                    titulo = titulo[0]
                
                nombre_del_autor = obra_respuesta['artistDisplayName'],
                if type(nombre_del_autor) == str:
                    nombre_del_autor = nombre_del_autor.replace("(","").replace(")","").replace(",","")
                if nombre_del_autor == " " or nombre_del_autor == "":
                    nombre_del_autor = "No especificado"
                if type(nombre_del_autor) == tuple:
                    nombre_del_autor = nombre_del_autor[0]
                
                nacionalidad_del_autor = obra_respuesta['artistNationality'],
                if nacionalidad_del_autor == " " or nacionalidad_del_autor == "":
                    nacionalidad_del_autor = "No especificada"
                if type(nacionalidad_del_autor) == tuple:
                    nacionalidad_del_autor = nacionalidad_del_autor[0]
                
                fecha_de_nacimiento = obra_respuesta['artistBeginDate'],
                if fecha_de_nacimiento == " " or fecha_de_nacimiento == "":
                    fecha_de_nacimiento = "No especificada"
                if type(fecha_de_nacimiento) == tuple:
                    fecha_de_nacimiento = fecha_de_nacimiento[0]
                
                fecha_de_muerte = obra_respuesta['artistEndDate'],
                if fecha_de_muerte == " " or fecha_de_muerte == "":
                    fecha_de_muerte = "No especificada"
                if type(fecha_de_muerte) == tuple:
                    fecha_de_muerte = fecha_de_muerte[0]
                
                tipo = obra_respuesta['classification'],
                if tipo == " " or tipo == "":
                    tipo = "No especificado"
                if type(tipo) == tuple:
                    tipo = tipo[0]
                
                año_de_creación = obra_respuesta['objectDate'],
                if año_de_creación == " " or año_de_creación == "":
                    año_de_creación = "No especificado"
                if type(año_de_creación) == tuple:
                    año_de_creación = año_de_creación[0]
                
                imagen_de_la_obra = obra_respuesta['primaryImage']
                if type(imagen_de_la_obra) == tuple:
                    imagen_de_la_obra = imagen_de_la_obra[0]
                    
                nueva_obra = Obra(
                    numero,
                    titulo,
                    nombre_del_autor,
                    nacionalidad_del_autor,
                    fecha_de_nacimiento,
                    fecha_de_muerte,
                    tipo,
                    año_de_creación,
                    imagen_de_la_obra,
                    )
                
                #Verifico que no este guardada
                guardada = False
                for obra in self.obras:
                    if obra.numero == nueva_obra.numero:
                        guardada = True
                        
                if not guardada:
                    self.obras.append(nueva_obra)
                    
                #Verifico el nombre del autor
                if nombre_autor.lower() not in nueva_obra.nombre_del_autor.lower():
                    ids_de_obras.remove(nueva_obra.numero)
            
            self.submenu_obras_por_nombre(nombre_autor,ids_de_obras)
        
    
    def menu(self):
        """ Metodo para imprimir el menu principal del sistema
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
        """
        while True:
            print(" ")
            print("---------- Sistema de catálogo de la colección de arte ----------")
            print(" ")
            elegida = imprimir_menu("Busqueda por departamento","Busqueda por nacionalidad del autor","Busqueda por nombre del autor")
            while not es_numero(elegida):
                print(" ")
                print("Intente de nuevo.")
                print(" ")
                elegida = imprimir_menu("Busqueda por departamento","Busqueda por nacionalidad del autor","Busqueda por nombre del autor")
                
            # por departamento
            if elegida == '1':
                print(" ")
                self.busqueda_por_departamento()
            
            # por nacionalidad del autor
            elif elegida == '2':
                print(" ")
                self.busqueda_por_nacionalidad_del_autor()
            
            # por nombre del autor
            elif elegida == '3':
                print(" ")
                self.busqueda_por_nombre_del_autor()
            
            elif elegida == '4':
                break
            
            else:
                print(" ")                
                print("Opción no válida. Intente de nuevo.")
                print(" ")
        
        
                
         