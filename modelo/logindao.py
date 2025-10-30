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
        
        sp = "exec [dbo].[sp_validar_usuario] @usuario=?, @contrasena_plana=?"
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

    def registrar_usuario(self, usuario, contrasena):
        """
        Registra un nuevo usuario en la base de datos.
        Retorna 1 si es exitoso, 0 si el usuario ya existe.
        """
        resultado = 0  
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        
        sp = "exec [dbo].[sp_registrar_usuario] @usuario=?, @contrasena_plana=?"
        param = [usuario, contrasena]
        
        try:
            cursor.execute(sp, param)
            
            fila = cursor.fetchone()
            if fila:
                resultado = int(fila[0])
                
            cursor.commit()
            
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            cursor.rollback() 
        finally:
            cursor.close()
            self.bd.cerrarConexionBD()
            
        return resultado