import sys
from PyQt5 import QtWidgets
from ui.ui_impl.ui_dimensoner_class import PDFDimensionerApp
from ui.ui_impl.ui_paginator_class import PDFPaginatorApp


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    dimensioner_window = PDFDimensionerApp()
    dimensioner_window.show()

    paginator_window = PDFPaginatorApp()
    paginator_window.show()

    sys.exit(app.exec_())
