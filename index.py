import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox
)
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter
import os

class PhotoEditor(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize UI components
        self.initUI()
        
        # Variables to store images
        self.original_image = None
        self.edited_image = None

    def initUI(self):
        self.setWindowTitle("Photo Editor")
        self.setGeometry(100, 100, 600, 400)

        # Create layout
        layout = QVBoxLayout()

        # Instruction label
        self.instruction_label = QLabel("Select an image file to edit", self)
        layout.addWidget(self.instruction_label)

        # Label to display original image
        self.original_image_label = QLabel("Original Image", self)
        layout.addWidget(self.original_image_label)

        # Label to display edited image
        self.edited_image_label = QLabel("Edited Image", self)
        layout.addWidget(self.edited_image_label)

        # Select File button
        select_button = QPushButton("Select File", self)
        select_button.clicked.connect(self.select_file)
        layout.addWidget(select_button)

        # Save Button
        save_button = QPushButton("Save Image", self)
        save_button.clicked.connect(self.save_image)
        layout.addWidget(save_button)

        # Set the layout for the widget
        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", 
            "Image files (*.jpg *.jpeg *.png *.bmp *.tiff *.gif)")
        
        if file_path:
            self.process_image(file_path)
        else:
            QMessageBox.warning(self, "Warning", "No file selected. Please select an image file.")

    def process_image(self, file_path):
        try:
            # Open the image using PIL
            self.original_image = Image.open(file_path)

            # Display original image
            self.display_image(self.original_image, self.original_image_label)

            # Apply SHARPEN filter
            self.edited_image = self.original_image.filter(ImageFilter.SHARPEN)

            # Display edited image
            self.display_image(self.edited_image, self.edited_image_label)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process the image: {e}")

    def display_image(self, image, label):
        # Convert the image to QPixmap for displaying in QLabel
        image = image.convert("RGBA")
        image.save("temp_image.png")  # Save temporarily to convert
        pixmap = QPixmap("temp_image.png")
        label.setPixmap(pixmap.scaled(200, 200))

    def save_image(self):
        if self.edited_image:
            try:
                downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                clean_name = os.path.splitext(os.path.basename("temp_image.png"))[0]
                edited_file_path = os.path.join(downloads_dir, f"{clean_name}_edited.png")

                # Save the edited image
                self.edited_image.save(edited_file_path)
                QMessageBox.information(self, "Success", f"Image saved to {edited_file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save the image: {e}")
        else:
            QMessageBox.warning(self, "Warning", "No edited image to save.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = PhotoEditor()
    editor.show()
    sys.exit(app.exec_())
