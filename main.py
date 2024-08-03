import sys
from PyQt5 import QtWidgets
from ui.ui_impl.ui_dimensoner_class import PDFDimensionerApp
from ui.ui_impl.ui_paginator_class import PDFPaginatorApp
from modules.page_info_service import get_outer_bbox

if __name__ == "__main__":
    ob = get_outer_bbox("new_test_dimension.pdf", 0)
    print(f"Widht: {ob.width}, Height {ob.height}")
    print(f"x0: {ob.x0}. y0={ob.y0}, x1: {ob.x1}, y1: {ob.y1} ")
    app = QtWidgets.QApplication(sys.argv)

    dimensioner_window = PDFDimensionerApp()
    dimensioner_window.show()

    paginator_window = PDFPaginatorApp()
    paginator_window.show()

    sys.exit(app.exec_())
