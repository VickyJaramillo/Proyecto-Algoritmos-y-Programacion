class Obra:
    def __init__(self, numero, titulo, nombre_del_autor, nacionalidad_del_autor, fecha_de_nacimiento, fecha_de_muerte, tipo, año_de_creación, imagen_de_la_obra):
        self.numero = numero
        self.titulo = titulo
        self.nombre_del_autor = nombre_del_autor
        self.nacionalidad_del_autor = nacionalidad_del_autor
        self.fecha_de_nacimiento = fecha_de_nacimiento
        self.fecha_de_muerte = fecha_de_muerte
        self.tipo = tipo
        self.año_de_creación = año_de_creación
        self.imagen_de_la_obra = imagen_de_la_obra
        
    def mostrar_para_listado(self):
        print(f'Obra #{self.numero}: "{self.titulo}". Nombre del autor: {self.nombre_del_autor}')
        
    def mostrar_detalles_completos(self):
        print(f"""
              Obra #{self.numero}: 
              Titulo {self.titulo} 
              Nombre del autor: {self.nombre_del_autor} 
              Nacionalidad del autor: {self.nacionalidad_del_autor} 
              Fecha de nacimiento: {self.fecha_de_nacimiento} 
              Fecha de muerte: {self.fecha_de_muerte} 
              Tipo: {self.tipo} 
              Año de creación: {self.año_de_creación} 
              Imagen de la obra: {self.imagen_de_la_obra}
              """)
        
        