import sys
from PyQt5 import QtWidgets
from ui.ui_impl.ui_implementation import App

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
