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
          
