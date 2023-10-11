from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QPushButton, QFileDialog, QLineEdit
import os
from Usd_Backpack import file_resolve




def apply_StyleSheet(class_obj):
    class_obj.setStyleSheet("""

            QMainWindow {
                background-color:#0E0D26;

            }



            QWidget {
                background-color:#0E0D26;

            }
            
            QLineEdit {
                background-color:#0E0D26;
                color:#77F289;

            }

            QLabel {
                color:#77F289;
                font-size:18px;
                font-weight:bold


            }

            QLineEdit {
                padding:6px;
                border:2px solid #aaa;
                border-radius: 5px;

            }

            /* Button Styling */
            QPushButton {
                padding: 8px 16px;
                background-color: #4B58A6;
                color:white;
                font-size: 18px;
                border:none;
                border-radius: 5px;


            }


            QPushButton:hover {
                background-color: #45a049;



            }


            QPushButton:pressed {
                background-color: #4B58A6;



            }

            QCheckBox {

                color:#77F289;
                font-size: 18px;

            }
            QCheckBox::indicator {
                background-color: #3F52BF;

            }

            QCheckBox::indicator:checked {
                background-color: #77F289;
            }

        """)

# file_resolve()
class UI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.window = uic.loadUi(file_resolve("code/ui_scripts/main_backpack_ui_v001_01.ui"), self)

        # setting up window icon
        icon = QIcon(file_resolve("code/ui_scripts/1652262321502.jpg"))
        self.window.setWindowIcon(icon)

        self.QWidget = self.findChild(QWidget, "centralwidget")
        self.label_result = self.findChild(QLabel, "label_main_name")
        self.lineEdit_input_usd = self.findChild(QLineEdit, "lineEdit_input_usd")

        self.input_usd_lable = self.findChild(QLabel, "label_input_usd")
        self.input_usd_browser_button = self.findChild(QPushButton, "pushButton_input_usd_browser")

        self.input_usd_browser_button.clicked.connect(lambda: self.open_file_dialog(self.lineEdit_input_usd))

    def open_file_dialog(self, line_edit_filed):
        file_dialog = QFileDialog()
        file_dialog.setDirectory("E:/Tools/USDA_backpack/test_cases/usd_backpack_test_cases/Simple_tester/Sceene") # Todo delet debug line
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")
        if str(file_path).endswith((".usd", ".usda", ".usdc")):
            line_edit_filed.setText(str(file_path))




app = QApplication([])
window = UI()
apply_StyleSheet(window)

window.show()
app.exec()
