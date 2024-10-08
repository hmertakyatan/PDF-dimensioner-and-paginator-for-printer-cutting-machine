import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from PyPDF2 import PdfReader, PdfWriter
from ui.qt.ui_pagination_window import Ui_PaginatorWindow
from modules import paginator
import traceback
import pymupdf
class PDFPaginatorApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PaginatorWindow()
        self.setWindowTitle("Main Window")
        self.ui.setupUi(self)
        self.selected_files = []

        # Connect buttons to their functions
        self.ui.addPdfDimensioned.clicked.connect(self.browse_files)
        self.ui.pushButton_2.clicked.connect(self.create_pdf)

    def browse_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Open PDF Files", "", "PDF Files (*.pdf)")
        self.selected_files = files  # Update the list of selected files

        if not self.selected_files:
            QMessageBox.warning(self, "Warning", "No files selected.")
            return

        # You can display selected files in a widget if needed
        # For example, update a list widget with file names (optional)

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

            output_width_text = self.ui.lineEdit_outpu_widht.text()
            output_height_text = self.ui.lineEdit_output_height.text()


            output_width = safe_convert_to_float(output_width_text)
            output_height = safe_convert_to_float(output_height_text)


            if None in [output_width, output_height]:
                QMessageBox.critical(self, "Error", "Invalid input for dimensions. Please enter valid numbers.")
                return

            if not self.selected_files:
                QMessageBox.critical(self, "Error", "No input PDF files selected.")
                return

            output_doc = pymupdf.open()
            for input_path in self.selected_files:
                if not os.path.isfile(input_path):
                    QMessageBox.critical(self, "Error", f"File not found: {input_path}")
                    return

            doc = paginator.paginate_labels_same_dimension(input_path, output_width, output_height)
            output_doc.insert_pdf(doc)
            output_doc.save(output_path)
            output_doc.close()    


            QMessageBox.information(self, "Success", "PDF created successfully!")
        except Exception as e:
            error_message = traceback.format_exc()
            print("Error occurred:\n", error_message)
            QMessageBox.critical(self, "Error", str(e))