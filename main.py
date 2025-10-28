import sys
from PyQt5 import QtWidgets
from load.load_ui_login import LoginWindow  

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login_ventana = LoginWindow()
    login_ventana.show()
    
    sys.exit(app.exec_())