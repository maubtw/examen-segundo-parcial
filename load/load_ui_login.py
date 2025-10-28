import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from modelo.logindao import LoginDao
from load.load_ui_productos import Load_ui_productos 

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login2.ui", self) 

        self.logindao = LoginDao()
        self.ventana_productos = None 
        
        self.btn_login.clicked.connect(self.handle_login)
        self.btn_page_productos.clicked.connect(self.abrir_modulo_productos)
        # self.btn_page_proveedores.clicked.connect(self.abrir_modulo_proveedores)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

    def handle_login(self):
        """
        Se ejecuta al presionar 'Iniciar Sesion'
        """
        usuario = self.usuario.text() 
        contra = self.contra.text()   

        if not usuario or not contra:
            print("Campos vacíos")
            # self.label_error.setText("Usuario y contraseña son requeridos.")
            return

        # Validar en la base de datos
        resultado_validacion = self.logindao.validar_usuario(usuario, contra)

        if resultado_validacion:
            print("Login exitoso")
            self.stackedWidget.setCurrentWidget(self.page_2)
            # self.label_error.setText("")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)  # Icono de error
            msg.setWindowTitle("Error de login")
            msg.setText("Usuario o contraseña incorrectos")
            msg.exec_()
            print("Login fallido")


    def abrir_modulo_productos(self):
            """
            Se ejecuta al presionar 'Productos' en el menú (page_2)
            """
            # 1. Oculta el menú en lugar de cerrarlo
            self.hide()
            
            # 2. Crea la ventana de productos
            # (Asegúrate de guardarla como 'self.ventana_productos')
            self.ventana_productos = Load_ui_productos()
            
            # --- LÍNEA CLAVE ---
            # 3. Conecta la señal de "regresar" de la ventana de productos
            #    a la función 'show' de ESTA ventana (login/menú).
            self.ventana_productos.regresar_al_menu_signal.connect(self.show)
            # ------------------
            
            # 4. Muestra la ventana de productos
            self.ventana_productos.show()
            



    # def abrir_modulo_proveedores(self):
    #     print("Abriendo módulo de proveedores...")
    #     # Aquí iría la lógica para la otra ventana
    #     pass