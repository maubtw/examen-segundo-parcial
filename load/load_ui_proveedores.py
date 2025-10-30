from modelo.proveedordao import Proveedordao
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QHeaderView

class Load_ui_proveedores(QtWidgets.QMainWindow):
    regresar_al_menu_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/ui_provedores.ui", self)
        self.proveedordao = Proveedordao()

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        self.boton_salir2.clicked.connect(self.volver_al_menu)
        self.frame_superior2.mouseMoveEvent = self.mover_ventana
        self.boton_menu2.clicked.connect(self.mover_menu)
        self.tabla_consulta2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Botones para cambiar de página
        self.boton_agregar2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_agregar2))
        self.boton_buscar2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_buscar2))
        self.boton_actualizar2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_actualizar2))
        self.boton_eliminar2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_eliminar2))
        self.boton_consultar2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_consultar2))

        # Botones de acciones
        self.accion_agregar2.clicked.connect(self.guardar_proveedor)
        self.accion_actualizar2.clicked.connect(self.guardar_cambios_proveedor)
        self.accion_eliminar2.clicked.connect(self.eliminar_proveedor)
        self.buscar_buscar2.clicked.connect(self.buscar_proveedor_buscar)
        self.buscar_eliminar2.clicked.connect(self.buscar_eliminar_proveedor)
        self.buscar_actualizar2.clicked.connect(self.actualizar_proveedor)
        self.accion_limpiar2.clicked.connect(self.limpiar_buscar)
        self.boton_refresh2.clicked.connect(self.actualizar_tabla)

    # Operaciones con el modelo de datos
    def guardar_proveedor(self):
            
            # 1. Obtener datos de los campos
            clave = self.sku_agregar2.text()
            nombre = self.descripcion_agregar2.text()
            telefono = self.existencia_agregar2.text()
            email = self.precio_agregar2.text()

            # 2. Validación simple (clave y nombre son obligatorios)
            if not clave or not nombre:
                # Asumo que tu label se llama 'label2' como indicaste
                self.label2.setText("Error: Clave y Nombre son obligatorios.")
                return

            try:
                # 3. Asignar datos al DAO
                self.proveedordao.proveedor.clave = clave
                self.proveedordao.proveedor.nombre = nombre
                self.proveedordao.proveedor.telefono = telefono
                self.proveedordao.proveedor.email = email
                
                # 4. Intentar insertar
                self.proveedordao.insertarProveedor()
                
                # 5. Éxito: Mostrar mensaje y limpiar formulario
                self.label2.setText("Proveedor Agregado con Éxito")
                self.sku_agregar2.clear()
                self.descripcion_agregar2.clear()
                self.existencia_agregar2.clear()
                self.precio_agregar2.clear()

            except Exception as e:
                # 6. Fracaso: Mostrar error
                # Muestra un error más amigable en la UI
                self.label2.setText("Error al agregar. Verifique los datos.")
                # Imprime el error técnico en la consola para ti
                print(f"Error en guardar_proveedor: {e}")
    def actualizar_proveedor(self):
        clave_a_buscar = self.sku_actualizar2.text()
        self.proveedordao.proveedor.nombre = clave_a_buscar
        resultados = self.proveedordao.buscar_proveedor()
        if resultados:
            proveedor_encontrado = resultados[0]
            self.proveedordao.proveedor.id_proveedor = int(proveedor_encontrado[0])
            self.descripcion_actualizar2.setText(str(proveedor_encontrado[2]))
            self.existencia_actualizar2.setText(str(proveedor_encontrado[3]))
            self.precio_actualizar2.setText(str(proveedor_encontrado[4]))
            self.tabla_consulta2.setRowCount(1)
            self.tabla_consulta2.setItem(0, 0, QtWidgets.QTableWidgetItem(str(proveedor_encontrado[1])))
            self.tabla_consulta2.setItem(0, 1, QtWidgets.QTableWidgetItem(str(proveedor_encontrado[2])))
            self.tabla_consulta2.setItem(0, 2, QtWidgets.QTableWidgetItem(str(proveedor_encontrado[3])))
            self.tabla_consulta2.setItem(0, 3, QtWidgets.QTableWidgetItem(str(proveedor_encontrado[4])))
            
        else:
            self.label2.setText("PROVEEDOR NO ENCONTRADO")

    def guardar_cambios_proveedor(self):
        clave = self.sku_actualizar2.text()
        nombre = self.descripcion_actualizar2.text()
        telefono = self.existencia_actualizar2.text()
        email = self.precio_actualizar2.text()
        
        self.proveedordao.proveedor.clave = clave
        self.proveedordao.proveedor.nombre = nombre
        self.proveedordao.proveedor.telefono = telefono
        self.proveedordao.proveedor.email = email

        if self.proveedordao.proveedor.id_proveedor == 0:
            self.label2.setText("Error: Primero debes BUSCAR un proveedor válido.")
            return

        try:
            self.proveedordao.proveedor.clave = clave
            self.proveedordao.proveedor.nombre = nombre
            self.proveedordao.proveedor.telefono = telefono
            self.proveedordao.proveedor.email = email
        except ValueError:
            self.label2.setText("Error: Campos inválidos.")
            return

        try:
            self.proveedordao.actualizarProveedor()
            self.label2.setText("¡Proveedor actualizado con éxito!")
            self.sku_actualizar2.clear()
            self.descripcion_actualizar2.clear()
            self.existencia_actualizar2.clear()
            self.precio_actualizar2.clear()
            self.proveedordao.proveedor.id_proveedor = 0
        except Exception as e:
            print(f"Error al actualizar: {e}")

    def buscar_eliminar_proveedor(self):
        clave_a_buscar = self.sku_eliminar2.text()
        self.proveedordao.proveedor.nombre = clave_a_buscar
        resultados = self.proveedordao.buscar_proveedor()
        if resultados:
            proveedor_encontrado = resultados[0]
            self.proveedordao.proveedor.id_proveedor = int(proveedor_encontrado[0])
            self.descripcion_eliminar2.setText(str(proveedor_encontrado[2]))
            self.existencia_eliminar2.setText(str(proveedor_encontrado[3]))
            self.precio_eliminar2.setText(str(proveedor_encontrado[4]))
            self.descripcion_eliminar2.setEnabled(False)
            self.existencia_eliminar2.setEnabled(False)
            self.precio_eliminar2.setEnabled(False)
        else:
            self.proveedordao.proveedor.id_proveedor = 0
            self.label2.setText("PROVEEDOR NO ENCONTRADO")

    def eliminar_proveedor(self):
        if self.proveedordao.proveedor.id_proveedor == 0:
            self.label2.setText("Proveedor invalido")
            return
        try:
            self.proveedordao.eliminarProveedor()
            self.label2.setText("Proveedor eliminado con exito!")
            self.sku_eliminar2.clear()
            self.descripcion_eliminar2.clear()
            self.existencia_eliminar2.clear()
            self.precio_eliminar2.clear()
            self.proveedordao.proveedor.id_proveedor = 0
        except Exception as e:
            print(f"Error al eliminar: {e}")
            self.label2.setText("Error al agregar Proveedor")

    def limpiar_buscar(self):
        self.sku_buscar2.clear()
        self.descripcion_buscar2.clear()
        self.existencia_buscar2.clear()
        self.precio_buscar2.clear()
        self.tabla_consulta2.clearContents()
        self.tabla_consulta2.setRowCount(0)

    def buscar_proveedor_buscar(self):
        clave_a_buscar = self.sku_buscar2.text()
        self.proveedordao.proveedor.nombre = clave_a_buscar
        resultados = self.proveedordao.buscar_proveedor()
        if resultados:
            proveedor_encontrado = resultados[0]

            self.descripcion_buscar2.setText(str(proveedor_encontrado[2]))  # Nombre
            self.existencia_buscar2.setText(str(proveedor_encontrado[3]))   # Teléfono
            self.precio_buscar2.setText(str(proveedor_encontrado[4]))      # Email (índice 5)

            self.tabla_consulta2.setRowCount(1)
            self.tabla_consulta2.setItem(0, 0, QtWidgets.QTableWidgetItem(str(proveedor_encontrado[1])))  # Clave
            self.tabla_consulta2.setItem(0, 1, QtWidgets.QTableWidgetItem(str(proveedor_encontrado[2])))  # Nombre
            self.tabla_consulta2.setItem(0, 2, QtWidgets.QTableWidgetItem(str(proveedor_encontrado[3])))  # Teléfono
            self.tabla_consulta2.setItem(0, 3, QtWidgets.QTableWidgetItem(str(proveedor_encontrado[4])))  # Email (índice 5)
        else:
            self.label_mensaje2.setText("PROVEEDOR NO ENCONTRADO")


    def actualizar_tabla(self):
        datos = self.proveedordao.listarProveedores()
        self.tabla_consulta2.setRowCount(len(datos))
        self.tabla_consulta2.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.tabla_consulta2.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        fila = 0
        for item in datos:
            self.tabla_consulta2.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(item[1])))
            self.tabla_consulta2.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(item[2])))
            self.tabla_consulta2.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(item[3])))
            self.tabla_consulta2.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(item[4])))
            fila += 1

    def volver_al_menu(self):
        self.regresar_al_menu_signal.emit()
        self.close()

    # Mover ventana
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def mover_ventana(self, event):
        if not self.isMaximized():
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()
        if event.globalPos().y() <= 20:
            self.showMaximized()
        else:
            self.showNormal()

    # Mover menú lateral
    def mover_menu(self):
        if True:			
            width = self.frame_lateral2.width()
            widthb = self.boton_menu2.width()
            normal = 0
            if width==0:
                extender = 200
                self.boton_menu2.setText("Menú")
            else:
                extender = normal
                self.boton_menu2.setText("")
                
            self.animacion = QPropertyAnimation(self.frame_lateral2, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()
            
            self.animacionb = QPropertyAnimation(self.boton_menu2, b'minimumWidth')
        
            self.animacionb.setStartValue(width)
            self.animacionb.setEndValue(extender)
            self.animacionb.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacionb.start()