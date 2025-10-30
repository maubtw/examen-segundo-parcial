from modelo.proveedores import Proveedores
from modelo.conexiondb import ConexionBD

class Proveedordao:

    def __init__(self):
        self.bd = ConexionBD()
        self.proveedor = Proveedores()

    def listarProveedores(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'exec [dbo].[sp_listar_proveedores]'
        cursor.execute(sp)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas

    def insertarProveedor(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_agregar_proveedor] @nombre=?, @telefono=?, @direccion=?, @email=?"
        param = [
            self.proveedor.clave,
            self.proveedor.nombre,
            self.proveedor.telefono,
            self.proveedor.email
        ]
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, param)
        cursor.commit()
        self.bd.cerrarConexionBD()

    def buscar_proveedor(self):
        """
        Busca un proveedor por su NOMBRE.
        """
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()

   
        sp = 'exec [dbo].[sp_buscar_proveedor] @nombre=?'
        param = [self.proveedor.nombre]

        cursor.execute(sp, param)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas


    def actualizarProveedor(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_actualizar_proveedor] @id_proveedor=?, @nombre=?, @telefono=?, @direccion=?, @email=?"
        param = [
            self.proveedor.id_proveedor,
            self.proveedor.clave,
            self.proveedor.nombre,
            self.proveedor.telefono,
            self.proveedor.email
        ]
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, param)
        cursor.commit()
        self.bd.cerrarConexionBD()

    def eliminarProveedor(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_eliminar_proveedor] @id_proveedor=?"
        param = [self.proveedor.id_proveedor]
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp, param)
        cursor.commit()
        self.bd.cerrarConexionBD()
