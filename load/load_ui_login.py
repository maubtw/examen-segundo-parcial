import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from modelo.logindao import LoginDao
from load.load_ui_proveedores import Load_ui_proveedores
from load.load_ui_productos import Load_ui_productos 

class LoginWindow(QtWidgets.QMainWindow):
    regresar_al_menu_signal = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login2.ui", self) 
        
        # Asegura que inicia en la página de login (login)
        # Asumo que tu primera página se llama 'login'
        self.stackedWidget.setCurrentWidget(self.login) 
        
        self.logindao = LoginDao()
        self.ventana_productos = None 
        self.ventana_proveedores = None 
        # --- Botones Página Login (login) ---
        self.btn_login.clicked.connect(self.handle_login)
        # Botón "Registrarse" que te lleva a la página de registro
        self.btn_reg.clicked.connect(self.mostrar_pagina_registro)
        self.btn_exit.clicked.connect(self.cerrar_logn) # Tu botón de salir
        #self.btn_exit_reg.clicked.connect(self.cerrar_logn) 
        
        # --- Botones Página Registro (register_2) ---
        # Nombres tomados de tu captura de pantalla
        self.btn_reg_reg.clicked.connect(self.handle_register)
        self.btn_login_reg.clicked.connect(self.mostrar_pagina_login)
        # self.btn_exit_reg.clicked.connect(self.cerrar_logn) # <-- Descomenta si también tienes un botón de salir aquí

        # --- Botones Página Menú (page_2) ---
        self.btn_cerrarSesion.clicked.connect(self.cerrarSesion)
        self.btn_page_productos.clicked.connect(self.abrir_modulo_productos)
        self.btn_page_provedores.clicked.connect(self.abrir_modulo_proveedores)

        # Configuración de la ventana
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

    

    def mostrar_pagina_registro(self):
        """Navega a la página de registro (register_2)"""
        self.stackedWidget.setCurrentWidget(self.register_2)
        self.usuario.clear()
        self.contra.clear()

    def mostrar_pagina_login(self):
        """Navega de vuelta a la página de login (login)"""
        self.stackedWidget.setCurrentWidget(self.login)
        self.usuario_reg.clear()
        self.contra_reg.clear()

    def handle_register(self):
        """
        Se ejecuta al presionar el botón 'Registrarse' (btn_reg_reg).
        """
        
        usuario = self.usuario_reg.text()
        contra = self.contra_reg.text()

        # Validación
        if not usuario or not contra:
            QMessageBox.warning(self, "Campos incompletos", "Debes llenar todos los campos.")
            return
        
        try:
            resultado = self.logindao.registrar_usuario(usuario, contra)
            
            if resultado == 1:
                # Éxito
                QMessageBox.information(self, "Registro Exitoso", "¡Usuario registrado con éxito! Ya puedes iniciar sesión.")
                self.mostrar_pagina_login() # Regresa a la página de login
            else:
                # Falla (usuario ya existe)
                QMessageBox.critical(self, "Error de Registro", "El nombre de usuario ya existe. Por favor, elige otro.")
        
        except Exception as e:
            QMessageBox.critical(self, "Error de Base de Datos", f"No se pudo completar el registro: {e}")
            print(f"Error al llamar a registrar_usuario: {e}")


    def handle_login(self):
        """
        Se ejecuta al presionar 'Iniciar Sesion'
        """
        usuario = self.usuario.text() 
        contra = self.contra.text()

        if not usuario or not contra:
            # (Asegúrate de importar QMessageBox)
            QMessageBox.warning(self, "Campos incompletos", "Usuario y contraseña son requeridos.")
            return

        # Validar en la base de datos
        resultado_validacion = self.logindao.validar_usuario(usuario, contra)

        # --- ¡ESTA ES LA CORRECCIÓN! ---
        # Verificamos que 'resultado_validacion' no sea None Y
        # que el primer valor dentro de la tupla sea 1.
        
        if resultado_validacion and resultado_validacion[0] == 1:
            # Éxito: El SP devolvió (1,)
            print("Login exitoso")
            self.stackedWidget.setCurrentWidget(self.page_2)
            self.usuario.clear() # Limpia los campos
            self.contra.clear()
        else:
            # Fracaso: El SP devolvió (0,) o None
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error de login")
            msg.setText("Usuario o contraseña incorrectos")
            msg.exec_()
            print("Login fallido")
            
    def abrir_modulo_productos(self):
            """
            Se ejecuta al presionar 'Productos' en el menú (page_2)
            """
            self.hide()     
            self.ventana_productos = Load_ui_productos()
            self.ventana_productos.regresar_al_menu_signal.connect(self.show)

            self.ventana_productos.show()

    def abrir_modulo_proveedores(self):
        self.hide()
        self.ventana_proveedores = Load_ui_proveedores()
        self.ventana_proveedores.regresar_al_menu_signal.connect(self.show)
        self.ventana_proveedores.show()
    def cerrar_logn(self):
        self.close()

    def cerrarSesion(self):
        """
        Regresa del menú (page_2) a la página de login (login)
        """
        self.stackedWidget.setCurrentWidget(self.login)
