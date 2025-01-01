
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

        # Room Name
        self.layout.addWidget(QLabel("Room Name/Number"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Room Name/Number")
        self.layout.addWidget(self.name_input)

        # Room Type
        self.layout.addWidget(QLabel("Room Type"))
        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("Enter Room Type (e.g., Single, Double)")
        self.layout.addWidget(self.type_input)

        # Room Size
        self.layout.addWidget(QLabel("Room Size (e.g., sq ft or m²)"))
        self.size_input = QLineEdit()
        self.size_input.setPlaceholderText("Enter Size (e.g., 25.5)")
        self.layout.addWidget(self.size_input)

        # Rental Price
        self.layout.addWidget(QLabel("Rental Price"))
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Enter Rental Price")
        self.layout.addWidget(self.price_input)

        # Amenities
        self.layout.addWidget(QLabel("Amenities"))
        self.amenities_input = QLineEdit()
        self.amenities_input.setPlaceholderText("Enter Amenities (comma-separated)")
        self.layout.addWidget(self.amenities_input)

        # Save Button
        self.save_btn = QPushButton("Save Room")
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
