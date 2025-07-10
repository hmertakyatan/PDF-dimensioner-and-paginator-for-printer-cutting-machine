import os
import traceback
import pymupdf
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog,QMessageBox, QLineEdit, QWidget, QHBoxLayout, QLabel, QPushButton, QListWidgetItem
from ui.qt.ui import Ui_MainWindow
from utils.converter import convert_to_float, convert_to_int
from modules.dimensioner import scale_page_content
from modules.paginator import paginate_labels_same_dimension

class App(QtWidgets.QMainWindow):
    PAGE_INDEX_DIMENSIONER = 0
    PAGE_INDEX_PAGINATOR = 1
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.bind_events()
        self.pdf_files = {
            self.PAGE_INDEX_DIMENSIONER: [],
            self.PAGE_INDEX_PAGINATOR: []
        }
    #Event binder
    def bind_events(self):
        self.ui.BTN_DIMENSIONER.clicked.connect(self.go_to_dimensioner_page)
        self.ui.BTN_PAGINATOR.clicked.connect(self.go_to_paginator_page)
        self.ui.PAGINATOR_BTN_ADDPDF.clicked.connect(self.add_pdf_files)
        self.ui.DIMENSIONER_BTN_ADDPDF.clicked.connect(self.add_pdf_files)
        self.ui.DIMENSIONER_BTN_PROCCES_FILES.clicked.connect(self.dimension_proccess)
        self.ui.PAGINATOR_BTN_PROCCES_FILE.clicked.connect(self.paginate_proccess)
    #Transition beetwen pages.
    def go_to_dimensioner_page(self):
        self.ui.stackedWidget.setCurrentIndex(self.PAGE_INDEX_DIMENSIONER)
    def go_to_paginator_page(self):
        self.ui.stackedWidget.setCurrentIndex(self.PAGE_INDEX_PAGINATOR)
    #PDF list manipulations
    def add_pdf_files(self):
        current_page_index = self.ui.stackedWidget.currentIndex()
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDF Files", "", "PDF Files (*.pdf)")
        if files:
            existing_paths = {file["path"] for file in self.pdf_files[current_page_index]}
            new_files = [f for f in files if f not in existing_paths]
            if new_files:
                for f in new_files:
                    self.pdf_files[current_page_index].append({"path": f, "count": 1})
                self.update_pdf_files(current_page_index, new_files=new_files)
            else:
                QMessageBox.information(self, "Info", "Selected files are already added.")

    def update_pdf_files(self, page_index, new_files=None):
        if page_index == self.PAGE_INDEX_DIMENSIONER:
            list_widget = self.ui.dimensioner_pdf_widgetlist
        elif page_index == self.PAGE_INDEX_PAGINATOR:
            list_widget = self.ui.paginator_pdf_widgetlist
        else:
            return

        if new_files is None:
            return

        for file_path in new_files:
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(5, 5, 5, 5)
            layout.setSpacing(10)

            file_label = QLabel(os.path.basename(file_path))
            file_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Preferred)

            if page_index == self.PAGE_INDEX_DIMENSIONER:
                count_input = QLineEdit("1")
                count_input.setFixedWidth(120)
                count_input.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(count_input)
            else:
                count_input = None

            remove_button = QPushButton("✖")
            remove_button.setFixedWidth(50)
            remove_button.setStyleSheet("color: red; font-weight: bold;")

            layout.addWidget(file_label)
            layout.addWidget(count_input)
            layout.addWidget(remove_button)

            widget.file_path = file_path
            widget.quantity_edit = count_input
            widget.remove_button = remove_button

            item = QListWidgetItem(list_widget)
            item.setSizeHint(widget.sizeHint())
            list_widget.addItem(item)
            list_widget.setItemWidget(item, widget)

            remove_button.clicked.connect(lambda _, item=item, file_path=file_path, page_index=page_index: self.remove_pdf_file(item, file_path, page_index))

    def remove_pdf_file(self, item, file_path, page_index):
        list_widget = None
        if page_index == self.PAGE_INDEX_DIMENSIONER:
            list_widget = self.ui.dimensioner_pdf_widgetlist
        elif page_index == self.PAGE_INDEX_PAGINATOR:
            list_widget = self.ui.paginator_pdf_widgetlist

        if list_widget:
            row = list_widget.row(item)
            list_widget.takeItem(row)

        self.pdf_files[page_index] = [file for file in self.pdf_files[page_index] if file["path"] != file_path]

    #Services
    def dimension_proccess(self):
        try:
            output_pdf_path, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf)")
            if not output_pdf_path:
                return
            width_text = self.ui.dimensioner_width_linedit.text()
            height_text = self.ui.dimensioner_height_linedit.text()
            rotate_text = self.ui.dimensioner_rotate_linedit.text()

            if None in [width_text, height_text]:
                QMessageBox.critical(self, "Error", "Invalid input for dimensions. Please enter valid numbers.")
                return

            width = convert_to_float(width_text)
            height = convert_to_float(height_text)
            if not rotate_text:
                rotate = 0
            else:
                rotate = convert_to_float(rotate_text)

            input_pdfs = self.pdf_files[self.PAGE_INDEX_DIMENSIONER]
            if not input_pdfs:
                QMessageBox.critical(self, "Error", "No PDF files selected for dimension proccess.")
                return
        
            output_doc = pymupdf.open()
            for idx in range(self.ui.dimensioner_pdf_widgetlist.count()):
                item = self.ui.dimensioner_pdf_widgetlist.item(idx)
                widget = self.ui.dimensioner_pdf_widgetlist.itemWidget(item)
                if widget:
                    file_path = widget.file_path
                    quantity_text = widget.quantity_edit.text().strip()

                    if quantity_text == "":
                        quantity = 1
                    else:
                        if not quantity_text.isdigit():
                            QMessageBox.critical(self, "Error", f"Invalid quantity input: '{quantity_text}'. Please enter a positive integer.")
                            return
                        quantity = int(quantity_text)
                        if quantity <= 0:
                            QMessageBox.critical(self, "Error", f"Quantity must be a positive number, got {quantity}.")
                            return

                    doc = scale_page_content(
                        input_pdf_path=file_path,
                        new_height_mm=height,
                        new_width_mm=width,
                        quantity=quantity,
                        rotate=rotate
                    )
                    output_doc.insert_pdf(doc)
            output_doc.save(filename=output_pdf_path)
            output_doc.close
            QMessageBox.information(self, "Success", "PDF created successfully!")

        except Exception as e:
            error_message = traceback.format_exc()
            print("Error occurred:\n", error_message)
            QMessageBox.critical(self, "Error", str(e))

    def paginate_proccess(self):
        try:
            output_pdf_path, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf)")
            if not output_pdf_path:
                return
            width_text = self.ui.paginator_width_lineedit.text()
            height_text = self.ui.paginator_height_lineedit.text()
            distance_text = self.ui.paginator_distance_lineedit.text()

            if None in [width_text, height_text]:
                QMessageBox.critical(self, "Error", "Invalid input for paginaton. Please enter valid numbers.")
                return

            width = convert_to_float(width_text)
            height = convert_to_float(height_text)
            if not distance_text:
                distance = 0
            else:
                distance = convert_to_int(distance_text)

            input_pdfs = self.pdf_files[self.PAGE_INDEX_PAGINATOR]
            if not input_pdfs:
                QMessageBox.critical(self, "Error", "No PDF files selected for dimension proccess.")
                return
            output_doc = pymupdf.open()
            for pdf in input_pdfs:
                file_path = pdf["path"]
                doc = paginate_labels_same_dimension(
                    input_pdf_path=file_path,
                    output_page_width_mm=width,
                    output_page_height_mm=height,
                    distance_mm=distance
                )
                output_doc.insert_pdf(doc)
            output_doc.save(output_pdf_path)
            output_doc.close()
            QMessageBox.information(self, "Success", "PDF created successfully!")


        except Exception as e:    
            error_message = traceback.format_exc()
            print("Error occurred:\n", error_message)
            QMessageBox.critical(self, "Error", str(e))

            
        
                

    