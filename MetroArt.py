import requests

from Obra import Obra

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
        # self.nacionalidades = [] Confirmar esto
        
        
    def cargar_datos_API(self):
        """ Metodo para cargar los datos de la API del museo metropolitano de arte.
        Atributos:
            self (MetroArt): Instancia de la clase MetroArt.
        """        
        print(f'\n---------- Cargando ----------\n')
                
        #Cargo las obras
        url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
        respuesta = requests.get(url)
        datos = respuesta.json()
        # En la pagina hay 400 mil obras pero en la pagina de la api
        # dice que solo se pueden leer 80 por segundo
        # Preguntar al preparador, por ahora tome 10 obras
        auxiliar = 0
        for i in datos['objectIDs']:
            if auxiliar < 10:
                url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{i}"
                respuesta = requests.get(url)
                obra_respuesta = respuesta.json()
                
                # self, numero, 
                # titulo, nombre_del_autor, 
                # nacionalidad_del_autor, fecha_de_nacimiento, 
                # fecha_de_muerte, tipo, 
                # año_de_creación, imagen_de_la_obra
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
                auxiliar += 1
        
        print(f'\n---------- Carga finalizada. ----------\n')
        
        # print(self.obras[0].mostrar_para_listado())
        print(self.obras[0].mostrar_detalles_completos())
        
        #Cargo los departamentos
        url = "https://collectionapi.metmuseum.org/public/collection/v1/departments"
        respuesta = requests.get(url)
        datos = respuesta.json()
        for departamento in datos['departments']:
            self.departamentos.append(departamento['displayName'])
        
        print(self.departamentos)
        
        print(f'\n---------- Carga de departamentos finalizada. ----------\n')
      
# Funciones a implementar:
# 1. Busqueda de obras 
#    a. por departamento
#    b. por nacionalidad del autor
#    c. por nombre del autor
# 2. Mostrar detalles 

# Hacer menu
        
        
                
         