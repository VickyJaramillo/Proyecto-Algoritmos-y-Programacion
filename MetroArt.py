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
        self.obras_por_autor = {}

    def leer_api(self,url):
        """ Metodo para leer la API del museo metropolitano de arte.
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
            url (str): URL a leer.
        Retorna
        """
        while True:
            print('.',end="")
            try:
                respuesta = requests.get(url)
                if respuesta.status_code == 200:
                    datos = respuesta.json()
                    break
            except:
                time.sleep(1)
                continue
        return datos
        
    
    def cargar_datos_API(self):
        """ Metodo para cargar los datos de la API del museo metropolitano de arte.
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
        """        
        
        print(f'\n---------- Cargando desde la API ----------\n')        
        #Cargo los departamentos
        url = "https://collectionapi.metmuseum.org/public/collection/v1/departments"
        datos = self.leer_api(url)
        
        # La lista de departamentos sera una lista de diccionarios
        for departamento in datos['departments']:
            self.departamentos.append(departamento)
        
        print(f'\n---------- Carga finalizada. ----------\n')
    
    def cargar_datos_csv(self, archivo):
        """ Metodo para cargar las nacionalidades del archivo CSV.
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
            archivo (str): Ruta del archivo CSV a cargar.
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
                    
                # Si no seleccionó un departamento valido de la lista
                if obra_encontrada == False:
                    print('')
                    print("Número de obra no existente.")
                    continue
                
                print(obra_a_mostrar.mostrar_detalles_completos())
                
                # Para mostrar la imagen
                api_url = obra.imagen_de_la_obra
                titulo = obra.titulo.replace(" ", "_")  # Reemplazo espacios por guiones bajos para el nombre del archivo
                    
                self.mostrar_imagen(api_url,titulo)
            
    def busqueda_por_departamento(self):
        """ Metodo para la funcionalidad de busqueda por departamento.
            Imprime la lista de departamentos para que el usuario seleccione uno eligiendo un numero 
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
                
                # Si esta en el diccionario se procede a mostrar las obras USAR FUNCION
                if encontrado != -1:
                    
                    # lista es la que contiene las obras
                    ids_de_obras = self.obras_por_departamento[nombre_del_departamento]
 
                    self.submenu_obras_por_departamento(nombre_del_departamento, ids_de_obras)
                    
                    continue #Si la consiguió no hace buscar en la API, vuelve al bucle
                
            print("No almacenadas, se procede a buscar en la API")
            print(" ")    
            print("Recuperando obras desde la API. Espere por favor...") 
            # Busco las obras por ese departamento en la API
            url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?departmentId={numero_del_departamento_seleccionado}&q=cat"
            
            datos = self.leer_api(url)
            
            ids_de_obras = datos['objectIDs']
            
            self.obras_por_departamento[nombre_del_departamento] = ids_de_obras # Guardo los ids de obras del departamento
            print("")
            for numero_de_obra in ids_de_obras:
                print(f"    Obra numero {numero_de_obra}") 
                url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{numero_de_obra}"
                obra_respuesta = self.leer_api(url)
                    
                nueva_obra = Obra(
                    obra_respuesta['objectID'],
                    obra_respuesta['title'],
                    obra_respuesta['artistDisplayName'],
                    obra_respuesta['artistNationality'],
                    obra_respuesta['artistBeginDate'],
                    obra_respuesta['artistEndDate'],
                    obra_respuesta['classification'],
                    obra_respuesta['objectDate'],
                    obra_respuesta['primaryImage']
                    )
                self.obras.append(nueva_obra)
            
            self.submenu_obras_por_departamento(nombre_del_departamento, ids_de_obras)
    
                            
    def busqueda_por_nacionalidad_del_autor(self):
        while True:
            # Imprimo los departamentos y guardo la elección del usuario
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
                    # lista_obras = self.obras_por_departamento[nombre_del_departamento]

                    # Extraer a funcion / Utilizar funcion
                    
                    continue #Si la consiguió no hace buscar en la API, vuelve al bucle
                
            print("No almacenadas, se procede a buscar en la API")
            print(" ")    
            print("Recuperando obras desde la API. Espere por favor...") 
            
            # Busco las obras por ese nacionalidad en la API
            url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?artistOrCulture=true&q=Afghan"
            
            datos = self.leer_api(url)
            
            ids_de_obras = datos['objectIDs']
            
            # Las guardo en el nacionalidad
            self.obras_por_nacionalidad[nombre_de_la_nacionalidad] = ids_de_obras
            print("")
            for numero_de_obra in ids_de_obras: 
                url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{numero_de_obra}"
                obra_respuesta = self.leer_api(url)
                    
                nueva_obra = Obra(
                    obra_respuesta['objectID'],
                    obra_respuesta['title'],
                    obra_respuesta['artistDisplayName'],
                    obra_respuesta['artistNationality'],
                    obra_respuesta['artistBeginDate'],
                    obra_respuesta['artistEndDate'],
                    obra_respuesta['classification'],
                    obra_respuesta['objectDate'],
                    obra_respuesta['primaryImage']
                    )
                self.obras.append(nueva_obra)
            
            # Extraer a funcion
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
                if int(numero_de_la_obra_a_mostrar) == '0': 
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
                
                # TODO: validar
                eleccion_mostrar_imagen = input('''
                ¿Desea ver la imagen de la obra en una nueva ventana? Ingrese "y" si lo desea o "n" en caso contrario:''')
                if eleccion_mostrar_imagen.lower() == "y":
                    # Funcion de mostrar imagen
                    # TODO: MOSTRAR IMAGEN
                    
                    # URL de la API 
                    api_url = obra.imagen_de_la_obra
                    # Nombre deseado para el archivo (sin extensión, ya que se determinará automáticamente) 
                    nombre_archivo_destino = "imagenes/logo_aleatorio" 
                    # Llamar a la función para guardar la imagen 
                    nombre_archivo_destino=guardar_imagen_desde_url(api_url, nombre_archivo_destino) 
                    img = Image.open(nombre_archivo_destino) 
                    img.show()
                    
                    print('imagen')
        
            
    def busqueda_por_nombre_del_autor(self):
        pass
    
    def menu(self):
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
                pass
            
            elif elegida == '4':
                break
            
            else:
                print(" ")                
                print("Opción no válida. Intente de nuevo.")
                print(" ")
            
        
            
# Funciones a implementar:
# 1. Busqueda de obras 
#    a. por departamento
#    b. por nacionalidad del autor
#    c. por nombre del autor
# 2. Mostrar detalles 

# Hacer menu
        
        
                
         