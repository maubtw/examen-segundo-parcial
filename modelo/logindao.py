from modelo.conexiondb import ConexionBD

class LoginDao:

    def __init__(self):
        self.bd = ConexionBD()

    def validar_usuario(self, usuario, contrasena):
        """
        Valida las credenciales del usuario contra la BD.
        Retorna el resultado de fetchone() (una tupla si es exitoso, None si falla).
        """
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        
        sp = "exec [dbo].[sp_validar_usuario] @usuario=?, @contrasena=?"
        param = [usuario, contrasena]
        
        try:
            cursor.execute(sp, param)
            resultado = cursor.fetchone() 
        except Exception as e:
            print(f"Error al validar usuario: {e}")
            resultado = None
        finally:
            cursor.close()
            self.bd.cerrarConexionBD()
            
        return resultado