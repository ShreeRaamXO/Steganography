from PyQt5 import QtWidgets, QtGui
from funcs import encode_image, decode_image
import sys
#idhi gpt 
class SteganographyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Steganography Tool')
        self.setGeometry(100, 100, 500, 300)

        layout = QtWidgets.QVBoxLayout()

        # Image Selection
        self.image_label = QtWidgets.QLabel('No image selected.')
        layout.addWidget(self.image_label)
        select_image_btn = QtWidgets.QPushButton('Select Image')
        select_image_btn.clicked.connect(self.select_image)
        layout.addWidget(select_image_btn)

        # Buttons
        embed_btn = QtWidgets.QPushButton('Embed Data')
        embed_btn.clicked.connect(self.embed_data)
        layout.addWidget(embed_btn)

        extract_btn = QtWidgets.QPushButton('Extract Data')
        extract_btn.clicked.connect(self.extract_data)
        layout.addWidget(extract_btn)

        # Output
        self.result_label = QtWidgets.QLabel('')
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def select_image(self):
        self.image_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image', '', 'PNG Files (*.png)')
        if self.image_path:
            self.image_label.setText(f'Selected: {self.image_path}')

    def embed_data(self):
        if not hasattr(self, 'image_path') or not self.image_path:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please select an image first!')
            return
        data, ok = QtWidgets.QInputDialog.getText(self, 'Embed Data', 'Enter data to embed:')
        if ok:
            save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Image', '', 'PNG Files (*.png)')
            if save_path:
                try:
                    encode_image(self.image_path, data, save_path)
                    QtWidgets.QMessageBox.information(self, 'Success', f'Data embedded and saved to {save_path}')
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def extract_data(self):
        if not hasattr(self, 'image_path') or not self.image_path:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please select an image first!')
            return
        try:
            hidden_data = decode_image(self.image_path)
            self.result_label.setText(f'Decoded Data: {hidden_data}')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SteganographyApp()
    window.show()
    sys.exit(app.exec_())
