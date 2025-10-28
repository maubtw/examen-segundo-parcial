from  modelo.producto import Producto
from modelo.conexiondb import ConexionBD

class Productodao:

    def __init__(self):
        self.bd = ConexionBD()
        self.producto = Producto()
    
    def listarProductos(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'exec [dbo].[sp_listar_productos]'
        cursor.execute(sp)
        filas = cursor.fetchall()

        self.bd.cerrarConexionBD()
        return filas 

    def insertarProducto(self):
        self.bd.establecerConexionBD()
        sp = "exec [dbo].[sp_insertar_producto] @clave=?, @descripcion=?, @existencia=?, @precio=? "
        param = [self.producto.clave, self.producto.descripcion, self.producto.existencia, self.producto.precio]
        cursor = self.bd.conexion.cursor()
        cursor.execute(sp,param)
        cursor.commit()
        self.bd.cerrarConexionBD()
    
    def buscar_producto(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'exec [dbo].[sp_buscar_productos] @clave=?'
        param = [self.producto.clave]
        cursor.execute(sp,param)
        filas = cursor.fetchall()

        self.bd.cerrarConexionBD()
        return filas         
    def actualizarProducto(self):
            self.bd.establecerConexionBD()
            sp = "exec [dbo].[sp_actualizar_producto] @id_producto=?, @clave=?, @descripcion=?, @existencia=?, @precio=?"
            
            param = [
                self.producto.id_producto,  
                self.producto.clave, 
                self.producto.descripcion, 
                self.producto.existencia, 
                self.producto.precio
            ]
            
            cursor = self.bd.conexion.cursor()
            print("Enviando parámetros para actualizar:", param) 
            cursor.execute(sp, param)
            cursor.commit()
            self.bd.cerrarConexionBD()

    def eliminarProducto(self):
         self.bd.establecerConexionBD()
         sp = "exec [dbo].[sp_eliminar_producto] @id_producto=?"
         param = [self.producto.id_producto]
         cursor = self.bd.conexion.cursor()
         cursor.execute(sp,param)
         cursor.commit()
         self.bd.cerrarConexionBD()