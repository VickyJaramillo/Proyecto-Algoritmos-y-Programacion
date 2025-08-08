def imprimir_menu(opcion1, opcion2, opcion3):
    print("Elija la opción deseada:")
    print(f"1. {opcion1}")
    print(f"2. {opcion2}")
    print(f"3. {opcion3}")
    print(f"4. Salir")
    seleccion = input("Seleccione una opción (1-4): ")
    return seleccion

def es_numero(numero):
        try:
                int(numero)
                return True
        except ValueError:
              return False
      
def es_nombre(nombre_autor):
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
                        
        
          
