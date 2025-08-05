import requests
import csv
import time

from Obra import Obra
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

    def cargar_datos_API(self):
        """ Metodo para cargar los datos de la API del museo metropolitano de arte.
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
        """        
        print(f'\n---------- Cargando desde la API ----------\n')
                
        # #Cargo las obras
        # url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
        # respuesta = requests.get(url)
        # datos = respuesta.json()
        # # En la pagina hay 400 mil obras pero en la pagina de la api
        # # dice que solo se pueden leer 80 por segundo
        # # Preguntar al preparador, por ahora tome 10 obras
        # auxiliar = 0
        # for i in datos['objectIDs']:
        #     if auxiliar < 10:
        #         url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{i}"
        #         respuesta = requests.get(url)
        #         obra_respuesta = respuesta.json()
                
        #         # self, numero, 
        #         # titulo, nombre_del_autor, 
        #         # nacionalidad_del_autor, fecha_de_nacimiento, 
        #         # fecha_de_muerte, tipo, 
        #         # año_de_creación, imagen_de_la_obra
        #         nueva_obra = Obra(
        #             obra_respuesta['objectID'],
        #             obra_respuesta['title'],
        #             obra_respuesta['artistDisplayName'],
        #             obra_respuesta['artistNationality'],
        #             obra_respuesta['artistBeginDate'],
        #             obra_respuesta['artistEndDate'],
        #             obra_respuesta['classification'],
        #             obra_respuesta['objectDate'],
        #             obra_respuesta['primaryImage']
        #         )
        #         self.obras.append(nueva_obra)
        #         auxiliar += 1
        
        # # print(self.obras[0].mostrar_para_listado())
        # print(self.obras[0].mostrar_detalles_completos())
        
        #Cargo los departamentos
        url = "https://collectionapi.metmuseum.org/public/collection/v1/departments"
        while True:
            print('.')
            try:
                respuesta = requests.get(url)
                if respuesta.status_code == 200:
                    datos = respuesta.json()
                    break
            except:
                time.sleep(1)
                print("Hi")
                continue
        
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
        
        print(f'\n---------- Carga desde CSV finalizada. ----------\n')
        
    def busqueda_por_departamento(self):
        """ Metodo para la funcionalidad de busqueda por departamento.
            Imprime la lista de departamentos para que el usuario seleccione uno eligiendo un numero 
        """        
        while True:
            # Imprimo los departamentos y guardo la elección del usuario
            print('')
            print("---------- Busqueda por departamento ----------")
            print('')
            for departamento in self.departamentos:
                print(f"Departamento #{departamento['departmentId']}: {departamento['displayName']}")
            print('')
            
            numero_del_departamento_seleccionado = input("Ingrese el numero del departamento que desea consultar o el numero 0 para salir: ")
            
            # TODO: VALIDAR QUE ES UN NUMERO
            
            # Si decide salir 
            if numero_del_departamento_seleccionado == 0: 
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
            
            print(f"Buscando por {nombre_del_departamento} ")
            # Si es valido busco las obras
            if len(self.obras_por_departamento)>0:
                # Verifico si ya se buscó en algun momento
                encontrado = self.obras_por_departamento.get(nombre_del_departamento,-1)
                
                # Si esta en el diccionario se procede a mostrar las obras USAR FUNCION
                if encontrado != -1:
                    print("Entré")
                    print(nombre_del_departamento)
                    print(self.obras_por_departamento[nombre_del_departamento])
                    
                    # Extraer a funcion / Utilizar funcion
                
            # Si no se encontro se busca en la API
            else:  
                # Busco las obras por ese departamento en la API
                url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?departmentId={numero_del_departamento_seleccionado}&q=cat"
                while True:
                    try:
                        respuesta = requests.get(url)
                        if respuesta.status_code == 200:
                            datos = respuesta.json()
                            break                    
                    except:
                        time.sleep(1)
                        continue
    
                ids_de_obras = datos['objectIDs']
                
                # Las guardo en el departamento
                self.obras_por_departamento[nombre_del_departamento] = ids_de_obras
                
                for numero_de_obra in ids_de_obras: 
                    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{numero_de_obra}"
                    while True:
                        try:
                            respuesta = requests.get(url)
                            if respuesta.status_code == 200:
                                obra_respuesta = respuesta.json()
                                break                    
                        except:
                            time.sleep(1)
                            continue
                        
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
                    print(f"---------- Departamento {nombre_del_departamento} ----------")
                    print(" ")
                    for obra in self.obras:
                        if obra.numero in ids_de_obras:
                            print(obra.mostrar_para_listado())
                    print(" ")
                    numero_de_la_obra_a_mostrar = input("Ingrese el numero una obra para mostrar sus detalles o el numero 0 para salir: ")
                    #Verifico que el input es numerico

                    # Si decide salir 
                    if int(numero_de_la_obra_a_mostrar) == 0: 
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
                        print('imagen')
                    
    def submenu_obras_por_departamento(self, alojada_en_obras_por_departamento,nombre_departamento='',lista_ids=[]):
        pass
                            
    def busqueda_por_nacionalidad_del_autor(self):
        pass
            
    def busqueda_por_nombre_del_autor(self):
        pass
    
    def menu(self):
        print("---------- Sistema de catálogo de la colección de arte ----------")
        while True:
            elegida = int(imprimir_menu("Busqueda por departamento","Busqueda por nacionalidad del autor","Busqueda por nombre del autor"))
            
            # por departamento
            if elegida == 1:
                self.busqueda_por_departamento()
            
            # por nacionalidad del autor
            elif elegida == 2:
                pass
            # por nombre del autor
            elif elegida == 3:
                pass
            elif elegida == 4:
                break
            
        
            
# Funciones a implementar:
# 1. Busqueda de obras 
#    a. por departamento
#    b. por nacionalidad del autor
#    c. por nombre del autor
# 2. Mostrar detalles 

# Hacer menu
        
        
                
         