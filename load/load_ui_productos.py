#1.- Importar librerias
from modelo.productodao import Productodao
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets, uic  

#2.1- Cargar archivo .ui

class Load_ui_productos(QtWidgets.QMainWindow):
    regresar_al_menu_signal = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        # Cargar archivo .ui
        uic.loadUi("ui/ui_productos.ui", self)
        self.show()
        self.productodao = Productodao()
#3.- Configurar contenedores
       
        #eliminar barra y de titulo - opacidad
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        #Cerrar ventana
        self.boton_salir.clicked.connect(self.volver_al_menu)
        # mover ventana
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        #menu lateral
        self.boton_menu.clicked.connect(self.mover_menu)
        #Fijar ancho columnas
        self.tabla_consulta.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

#4.- Conectar botones a funciones

        #Botones para cambiar de página
        self.boton_agregar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_agregar))
        self.boton_buscar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_buscar))
        self.boton_actualizar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_actualizar))
        self.boton_eliminar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_eliminar))
        self.boton_consultar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_consultar))
        
        
        #Botones para guardar, buscar, actualizar, eliminar y salir
        #Botones para guardar, buscar, actualizar, eliminar y salir
        self.accion_agregar.clicked.connect(self.guardar_producto)
        self.accion_actualizar.clicked.connect(self.guardar_cambios_producto)
        self.accion_eliminar.clicked.connect(self.eliminar_producto)
        self.buscar_buscar.clicked.connect(self.buscar_producto_buscar)
        self.buscar_eliminar.clicked.connect(self.buscar_eliminar_producto)
        self.buscar_actualizar.clicked.connect(self.actualizar_producto)
        self.accion_limpiar.clicked.connect(self.limpiar_buscar)
        self.boton_refresh.clicked.connect(self.actualizar_tabla)

     
#5.- Operaciones con el modelo de datos
    def guardar_producto(self):
        """
        Funcion para agregar un producto
        """
        clave = self.sku_agregar.text()
        descripcion = self.descripcion_agregar.text()
        existencia_str = self.existencia_agregar.text()
        precio_str = self.precio_agregar.text()

        if not clave or not descripcion or not existencia_str or not precio_str:
            self.label.setText("Error: Todos los campos son obligatorios.")
            return

        try:
            self.productodao.producto.clave = clave
            self.productodao.producto.descripcion = descripcion
            self.productodao.producto.existencia = int(existencia_str)
            self.productodao.producto.precio = float(precio_str)
            
            self.productodao.insertarProducto()
            
            self.label.setText("Producto insertado con éxito")
            self.sku_agregar.clear()
            self.descripcion_agregar.clear()
            self.existencia_agregar.clear()
            self.precio_agregar.clear()

        except ValueError:
            self.label.setText("Error: Existencia o Precio deben ser números.")
        except Exception as e:
            self.label.setText("Error al insertar. Verifique los datos.")
            print(f"Error en guardar_producto: {e}")

        
    def actualizar_producto(self):
            """
            Funcion para recuperar un producto conforme a su SKU
            """
            clave_a_buscar = self.sku_actualizar.text() 
            self.productodao.producto.clave = clave_a_buscar

            resultados = self.productodao.buscar_producto() 

            if resultados:
                producto_encontrado = resultados[0]
                self.productodao.producto.id_producto = int(producto_encontrado[0])
                precio_formateado = "{:.2f}".format(float(producto_encontrado[4]))
                
                self.descripcion_actualizar.setText(str(producto_encontrado[2]))
                self.existencia_actualizar.setText(str(producto_encontrado[3])) 
                self.precio_actualizar.setText(str(precio_formateado))

            
                self.tabla_consulta.setRowCount(1)
                self.tabla_consulta.setItem(0, 0, QtWidgets.QTableWidgetItem(str(producto_encontrado[1]))) # Clave
                self.tabla_consulta.setItem(0, 1, QtWidgets.QTableWidgetItem(str(producto_encontrado[2]))) # Descripgfhm
                self.tabla_consulta.setItem(0, 2, QtWidgets.QTableWidgetItem(str(producto_encontrado[3]))) # Exisgfncia
                self.tabla_consulta.setItem(0, 3, QtWidgets.QTableWidgetItem(str(precio_formateado))) # Precio
                
            else:

                self.label.setText("PRODUCTO NO ENCONTRADO")

    def guardar_cambios_producto(self):
        """
        Funcion actualizar los cambios en la pestana buscar
        """
        clave = self.sku_actualizar.text()
        descripcion = self.descripcion_actualizar.text()
        existencia = self.existencia_actualizar.text()
        precio = self.precio_actualizar.text()

        if self.productodao.producto.id_producto == 0:
            print("Error: Primero debes BUSCAR un producto válido.")
            self.label.setText("Error: Primero debes BUSCAR un producto válido.")
            return

        try:

            self.productodao.producto.clave = clave
            self.productodao.producto.descripcion = descripcion
            self.productodao.producto.existencia = int(existencia)
            self.productodao.producto.precio = float(precio)
        except ValueError:
            print("Error: Existencia o Precio no son números válidos.")
            self.label.setText("Error: Existencia o Precio no son números válidos.")
            return

        try:
            self.productodao.actualizarProducto() 
            self.label.setText("¡Producto actualizado con éxito!")
            self.sku_actualizar.clear()
            self.descripcion_actualizar.clear()
            self.existencia_actualizar.clear()
            self.precio_actualizar.clear()
            self.productodao.producto.id_producto = 0 
            
        except Exception as e:
            self.label.setText(f"Error al actualizar: {e}")

    def buscar_eliminar_producto(self):
        clave_a_buscar = self.sku_eliminar.text() 
        self.productodao.producto.clave = clave_a_buscar

        resultados = self.productodao.buscar_producto() 

        if resultados:
            producto_encontrado = resultados[0]
            self.productodao.producto.id_producto = int(producto_encontrado[0])

            precio_formateado = "{:.2f}".format(float(producto_encontrado[4]))
            
            self.descripcion_eliminar.setText(str(producto_encontrado[2]))
            self.existencia_eliminar.setText(str(producto_encontrado[3])) 
            self.precio_eliminar.setText(str(precio_formateado))
        
            self.descripcion_eliminar.setEnabled(False)
            self.existencia_eliminar.setEnabled(False)
            self.precio_eliminar.setEnabled(False)

        else:
            self.productodao.producto.id_producto = 0 
            self.label.setText("PRODUCTO NO ENCONTRADO")
            self.existencia_eliminar.clear()
            self.precio_eliminar.clear()
            
            self.descripcion_eliminar.setEnabled(True)
            self.existencia_eliminar.setEnabled(True)
            self.precio_eliminar.setEnabled(True)
    
    def eliminar_producto(self):
        if self.productodao.producto.id_producto == 0:
            self.label.setText("Producto invalido")
            return
        try:
            self.productodao.eliminarProducto()
            self.label.setText("Producto eliminado con exito!")
            self.sku_eliminar.clear()
            self.descripcion_eliminar.clear()
            self.existencia_eliminar.clear()
            self.precio_eliminar.clear()

            self.descripcion_eliminar.setEnabled(True)
            self.existencia_eliminar.setEnabled(True)
            self.precio_eliminar.setEnabled(True)
            self.productodao.producto.id_producto = 0

        except Exception as e:
            print(f"Error al eliminar el producto: {e}")
            self.label.setText(f"Error al eliminar: {e}")
        
    def limpiar_buscar(self):
        """
        Limpia el formulario de buscar
        """
        self.sku_buscar.clear()
        self.descripcion_buscar.clear()
        self.existencia_buscar.clear()
        self.precio_buscar.clear()
        self.tabla_consulta.clearContents()
        self.tabla_consulta.setRowCount(0)     

    def buscar_producto_buscar(self):
            """
            Recupera los productos en la pestana buscar
            """
            clave_a_buscar = self.sku_buscar.text() 
            self.productodao.producto.clave = clave_a_buscar

            resultados = self.productodao.buscar_producto() 

            if resultados:
                producto_encontrado = resultados[0]
        
                precio_formateado = "{:.2f}".format(float(producto_encontrado[4]))
                print(precio_formateado)

                self.descripcion_buscar.setText(str(producto_encontrado[2]))
                self.existencia_buscar.setText(str(producto_encontrado[3])) 
                self.precio_buscar.setText(str(precio_formateado))

            
                self.tabla_consulta.setRowCount(1)
                self.tabla_consulta.setItem(0, 0, QtWidgets.QTableWidgetItem(str(producto_encontrado[1]))) # Clave
                self.tabla_consulta.setItem(0, 1, QtWidgets.QTableWidgetItem(str(producto_encontrado[2]))) # Descripgfhm
                self.tabla_consulta.setItem(0, 2, QtWidgets.QTableWidgetItem(str(producto_encontrado[3]))) # Exisgfncia
                self.tabla_consulta.setItem(0, 3, QtWidgets.QTableWidgetItem(str(precio_formateado))) # Precio
                
            else:

                self.descripcion_buscar.setText("PRODUCTO NO ENCONTRADO")

    def actualizar_tabla(self):
        """
        Funcion para ver la tabla de productos
        """
        datos = self.productodao.listarProductos()
        self.tabla_consulta.setRowCount(len(datos))
        fila = 0
        for item in datos:
            self.tabla_consulta.setItem(fila,0,QtWidgets.QTableWidgetItem(str(item[1])))
            self.tabla_consulta.setItem(fila,1,QtWidgets.QTableWidgetItem(str(item[2])))
            self.tabla_consulta.setItem(fila,2,QtWidgets.QTableWidgetItem(str(item[3])))
            self.tabla_consulta.setItem(fila,3,QtWidgets.QTableWidgetItem(str(item[4])))
            fila += 1

    def volver_al_menu(self):
        """
        Emite la señal para regresar al menú y cierra esta ventana.
        """
        self.regresar_al_menu_signal.emit() # 1. Avisa a la ventana de login
        self.close() # 2. Cierra esta ventana (Productos)
# 6.- mover ventana
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
    def mover_ventana(self, event):
        if self.isMaximized() == False:			
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

        if event.globalPos().y() <=20:
            self.showMaximized()
        else:
            self.showNormal()
#7.- Mover menú
    def mover_menu(self):
        if True:			
            width = self.frame_lateral.width()
            widthb = self.boton_menu.width()
            normal = 0
            if width==0:
                extender = 200
                self.boton_menu.setText("Menú")
            else:
                extender = normal
                self.boton_menu.setText("")
                
            self.animacion = QPropertyAnimation(self.frame_lateral, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()
            
            self.animacionb = QPropertyAnimation(self.boton_menu, b'minimumWidth')
        
            self.animacionb.setStartValue(width)
            self.animacionb.setEndValue(extender)
            self.animacionb.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacionb.start()