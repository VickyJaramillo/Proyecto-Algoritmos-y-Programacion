def imprimir_menu(opcion1, opcion2, opcion3):
        """ Metodo para imprimir un menu simple
        Atributos:
            opcion1 (str): opción a imprimir en el sistema de primera en la lista de opciones
            opcion2 (str): opción a imprimir en el sistema de segunda en la lista de opciones
            opcion3 (str): opción a imprimir en el sistema de tercera en la lista de opciones

        Retorna:
            selección: opcion elegida por el usuario
        """    
        print("Elija la opción deseada:")
        print(f"1. {opcion1}")
        print(f"2. {opcion2}")
        print(f"3. {opcion3}")
        print(f"4. Salir")
        seleccion = input("Seleccione una opción (1-4): ")
        return seleccion

def es_numero(numero):
        """ Metodo para la funcionalidad de busqueda por nombre del autor.
        Atributos:
                numero (str): el número a verificar si es un número entero o no.
        Retorna:
                True si el número es un número entero, False si no es un número entero.
        """
        try:
                int(numero)
                return True
        except ValueError:
              return False
      
def es_nombre(nombre_autor):
        """ Metodo para la funcionalidad de busqueda por nombre del autor.
        Atributos:
                nombre_autor (str): el nombre del autor a verificar si es un nombre o no.
        Retorna:
                True si el nombre es un nombre, False si no es un nombre.
        """
        if type(nombre_autor) == str:
                if " " in nombre_autor and nombre_autor.count(" ")==1:
                        nombre_autor_provisional=nombre_autor
                        copia=nombre_autor_provisional.replace(" ","")
                        if copia.isalpha() and len(nombre_autor)>=3 and len(nombre_autor)<=30:
                                return True
                        return False
                else:
                        if len(nombre_autor)>=3 and len(nombre_autor)<=30:
                                return True
                        return False
        else:
                return False        
        


          
