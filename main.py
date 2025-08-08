from MetroArt import MetroArt
def main():
    """Función para iniciar el sistema
    """    
    museo = MetroArt()
    museo.cargar_datos_csv("CH_Nationality_List_20171130_v1.csv")
    museo.cargar_datos_API()
    museo.menu()

main()
    