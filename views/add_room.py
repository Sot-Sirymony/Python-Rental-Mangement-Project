

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from controllers.room_controller import add_room

class AddRoomView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Room")
        self.resize(400, 400)
        self.setModal(True)  # Make the dialog modal

        self.layout = QVBoxLayout()

        # Shared stylesheet for labels
        label_style = "font-size: 16px; font-weight:bold;"

        # Room Name
        room_name_label = QLabel("Room Name/Number")
        room_name_label.setStyleSheet(label_style)
        self.layout.addWidget(room_name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Room Name/Number")
        self.name_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.name_input)

        # Room Type
        room_type_label = QLabel("Room Type")
        room_type_label.setStyleSheet(label_style)
        self.layout.addWidget(room_type_label)
        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("Enter Room Type (e.g., Single, Double)")
        self.type_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.type_input)

        # Room Size
        room_size_label = QLabel("Room Size (e.g., sq ft or m²)")
        room_size_label.setStyleSheet(label_style)
        self.layout.addWidget(room_size_label)
        self.size_input = QLineEdit()
        self.size_input.setPlaceholderText("Enter Size (e.g., 25.5)")
        self.size_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.size_input)

        # Rental Price
        rental_price_label = QLabel("Rental Price")
        rental_price_label.setStyleSheet(label_style)
        self.layout.addWidget(rental_price_label)
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Enter Rental Price")
        self.price_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.price_input)

        # Amenities
        amenities_label = QLabel("Amenities")
        amenities_label.setStyleSheet(label_style)
        self.layout.addWidget(amenities_label)
        self.amenities_input = QLineEdit()
        self.amenities_input.setPlaceholderText("Enter Amenities (comma-separated)")
        self.amenities_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.amenities_input)

        # Save Button
        self.save_btn = QPushButton("Save Room")
        self.save_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        self.save_btn.clicked.connect(self.save_room)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

    def save_room(self):
        """Save the room data to the database."""
        name = self.name_input.text().strip()
        room_type = self.type_input.text().strip()
        size = self.size_input.text().strip()
        rental_price = self.price_input.text().strip()
        amenities = self.amenities_input.text().strip()

        # Validation
        if not name:
            QMessageBox.warning(self, "Validation Error", "Please enter a room name/number.")
            return
        if not room_type:
            QMessageBox.warning(self, "Validation Error", "Please enter a room type.")
            return
        if not size or not size.replace(".", "", 1).isdigit() or float(size) <= 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid room size (positive number).")
            return
        if not rental_price or not rental_price.replace(".", "", 1).isdigit() or float(rental_price) <= 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid rental price (positive number).")
            return

        try:
            # Save room using the controller
            add_room(name, room_type, float(size), float(rental_price), amenities)
            QMessageBox.information(self, "Success", "Room added successfully!")
            self.accept()  # Close the dialog
        except Exception as e:
            print(f"Error adding room: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add room: {e}")
