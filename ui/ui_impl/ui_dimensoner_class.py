import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog,QMessageBox, QLineEdit, QWidget, QHBoxLayout, QLabel, QPushButton, QListWidgetItem
from PyPDF2 import PdfReader, PdfWriter
from ui.qt.ui_dimensioner_window import Ui_DimensionerWindow
from modules.dimensioner import scale_page_content
import traceback
from PyPDF2 import PdfReader, PdfWriter
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidgetItem, QWidget
import os
import pymupdf

class PDFDimensionerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DimensionerWindow()
        self.ui.setupUi(self)
        self.selected_files = []  # Listeyi burada tanımlıyoruz

        self.ui.pdfAdder.clicked.connect(self.browse_files)
        self.ui.pdfCreater.clicked.connect(self.create_pdf)

    def browse_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Open PDF Files", "", "PDF Files (*.pdf)")
        self.selected_files = files  # Seçilen dosyaları listeye ekliyoruz

        self.ui.pdfListWidget.clear()  # Listeyi temizle

        for file in files:
            item_widget = QWidget()
            item_layout = QHBoxLayout()
            item_widget.setLayout(item_layout)

            file_name = os.path.basename(file)
            file_label = QLabel(file_name)
            item_layout.addWidget(file_label)

            label_count_lineedit = QLineEdit()
            label_count_lineedit.setPlaceholderText("Enter count")
            item_layout.addWidget(label_count_lineedit)

            delete_button = QPushButton("X")
            delete_button.clicked.connect(lambda ch, item_widget=item_widget: self.remove_item(item_widget))
            item_layout.addWidget(delete_button)

            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.ui.pdfListWidget.addItem(item)
            self.ui.pdfListWidget.setItemWidget(item, item_widget)

    def remove_item(self, item_widget):
        for i in range(self.ui.pdfListWidget.count()):
            item = self.ui.pdfListWidget.item(i)
            if self.ui.pdfListWidget.itemWidget(item) == item_widget:
                self.ui.pdfListWidget.takeItem(i)
                break

    def create_pdf(self):
        try:
            output_path, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf)")
            if not output_path:
                return

            def safe_convert_to_float(text):
                try:
                    return float(text)
                except ValueError:
                    return None

            label_width_text = self.ui.lineEdit_widht.text()
            label_height_text = self.ui.lineEdit_height.text()

            label_width = safe_convert_to_float(label_width_text)
            label_height = safe_convert_to_float(label_height_text)

            if None in [label_width, label_height]:
                QMessageBox.critical(self, "Error", "Invalid input for dimensions. Please enter valid numbers.")
                return

            input_pdfs = []
            for i in range(self.ui.pdfListWidget.count()):
                item = self.ui.pdfListWidget.item(i)
                item_widget = self.ui.pdfListWidget.itemWidget(item)
                file_label = item_widget.layout().itemAt(0).widget()
                label_count_lineedit = item_widget.layout().itemAt(1).widget()
                try:
                    label_count = int(label_count_lineedit.text())
                except ValueError:
                    label_count = 1
                input_pdfs.append((self.selected_files[i], label_count))

            if not input_pdfs:
                QMessageBox.critical(self, "Error", "No input PDF files selected.")
                return
            
            output_doc = pymupdf.open()
            for input_pdf, count in input_pdfs:
                doc = scale_page_content(input_pdf, label_width, label_height, count)
                output_doc.insert_pdf(doc)   
            output_doc.save(output_path)
            output_doc.close()

            QMessageBox.information(self, "Success", "PDF created successfully!")
        except Exception as e:
            error_message = traceback.format_exc()
            print("Error occurred:\n", error_message)
            QMessageBox.critical(self, "Error", str(e))