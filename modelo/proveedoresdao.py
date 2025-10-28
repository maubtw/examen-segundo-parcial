from modelo.proveedores import Proveedores
from modelo.conexiondb import ConexionBD

class Proveedoresdao:
    
    def __init__(self):
        self.bd = ConexionBD()
        self.proveedor = Proveedores()

    def actualizar_proveedor(self, id_proveedor, nombre=None, telefono=None, direccion=None, email=None):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()

        sp = """
        EXEC [dbo].[sp_actualizar_proveedor]
            @id_proveedor = ?,
            @nombre = ?,
            @telefono = ?,
            @direccion = ?,
            @email = ?
        """
        cursor.execute(sp, (id_proveedor, nombre, telefono, direccion, email))
        self.bd.conexion.commit()  

        print(f"Proveedor {id_proveedor} actualizado correctamente.")

        self.bd.cerrarConexionBD()

    def agregar_proveedor(self, nombre=None, telefono=None, direccion=None, email=None):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = """
        EXEC [dbo].[sp_agregar_proveedor]
            @nombre = ?,
            @telefono = ?,
            @direccion = ?,
            @email = ?
        """
        cursor.execute(sp,(nombre, telefono, direccion, email))
        self.bd.conexion.commit()
        print(f"Proveedor {nombre} agregado")

        self.bd.cerrarConexionBD()

    def eliminar_proveedor(self, id_proveedor):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC [dbo].[sp_eliminar_proveedor] @id_proveedor =?"
        cursor.execute(sp,(id_proveedor))
        self.bd.conexion.commit()
        print(f"Proveedor con id: {id_proveedor} eliminado")

        self.bd.cerrarConexionBD()

    def listar_proveedores(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC [dbo].[sp_listar_proveedores]"
        cursor.execute(sp)
        filas = cursor.fetchall()
        for fila in filas: 
            print(fila)

        self.bd.cerrarConexionBD()

    

