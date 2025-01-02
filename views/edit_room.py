

from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QLabel, QDialog, QMessageBox, QComboBox
from controllers.room_controller import update_room


class EditRoomView(QDialog):
    def __init__(self, room_id, current_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Room")
        self.room_id = room_id
        self.setModal(True)  # Make the dialog modal
        self.layout = QVBoxLayout()

        # Error Label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-size: 14px;")
        self.layout.addWidget(self.error_label)

        # Shared stylesheet for labels
        label_style = "font-size: 16px;"

        # Room Name
        name_label = QLabel("Room Name:")
        name_label.setStyleSheet(label_style)
        self.layout.addWidget(name_label)
        self.name_input = QLineEdit(current_data.get('name', ''))
        self.name_input.setPlaceholderText("Enter Room Name")
        self.name_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.name_input)

        # Room Type
        type_label = QLabel("Room Type:")
        type_label.setStyleSheet(label_style)
        self.layout.addWidget(type_label)
        self.type_input = QLineEdit(current_data.get('type', ''))
        self.type_input.setPlaceholderText("Enter Room Type (e.g., Single, Double)")
        self.type_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.type_input)

        # Room Size
        size_label = QLabel("Room Size (e.g., sq ft or m²):")
        size_label.setStyleSheet(label_style)
        self.layout.addWidget(size_label)
        self.size_input = QLineEdit(current_data.get('size', ''))
        self.size_input.setPlaceholderText("Enter Room Size (e.g., 25.5)")
        self.size_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.size_input)

        # Rental Price
        price_label = QLabel("Rental Price:")
        price_label.setStyleSheet(label_style)
        self.layout.addWidget(price_label)
        self.price_input = QLineEdit(current_data.get('rental_price', ''))
        self.price_input.setPlaceholderText("Enter Rental Price")
        self.price_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.price_input)

        # Amenities
        amenities_label = QLabel("Amenities:")
        amenities_label.setStyleSheet(label_style)
        self.layout.addWidget(amenities_label)
        self.amenities_input = QLineEdit(current_data.get('amenities', ''))
        self.amenities_input.setPlaceholderText("Enter Amenities (comma-separated)")
        self.amenities_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.amenities_input)

        # Occupancy Status
        occupancy_label = QLabel("Occupancy Status:")
        occupancy_label.setStyleSheet(label_style)
        self.layout.addWidget(occupancy_label)
        self.occupancy_status_input = QComboBox()
        self.occupancy_status_input.addItems(["Available", "Rented", "Maintenance"])  # Example statuses
        self.occupancy_status_input.setCurrentText(current_data.get('occupancy_status', 'Available'))  # Set current status
        self.occupancy_status_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.occupancy_status_input)

        # Save Changes Button
        self.update_btn = QPushButton("Save Changes")
        self.update_btn.clicked.connect(self.save_changes)
        self.update_btn.setStyleSheet("font-size: 14px; padding: 8px;")
        self.layout.addWidget(self.update_btn)

        self.setLayout(self.layout)

    def save_changes(self):
        """Save changes to the room."""
        # Fetch input values
        name = self.name_input.text().strip()
        room_type = self.type_input.text().strip()
        size = self.size_input.text().strip()
        rental_price = self.price_input.text().strip()
        amenities = self.amenities_input.text().strip()
        occupancy_status = self.occupancy_status_input.currentText()  # Get the selected status

        # Validation
        if not name:
            self.error_label.setText("Error: Room Name is required.")
            return
        if not room_type:
            self.error_label.setText("Error: Room Type is required.")
            return
        if not size:
            self.error_label.setText("Error: Room Size is required.")
            return
        if not size.replace('.', '', 1).isdigit():
            self.error_label.setText("Error: Room Size must be a numeric value.")
            return
        if not rental_price:
            self.error_label.setText("Error: Rental Price is required.")
            return
        if not rental_price.replace('.', '', 1).isdigit():
            self.error_label.setText("Error: Rental Price must be a numeric value.")
            return

        try:
            # Convert validated input to appropriate types
            size = float(size)
            rental_price = float(rental_price)

            # Call the update function
            update_room(self.room_id, name, room_type, size, rental_price, amenities, occupancy_status)
            QMessageBox.information(self, "Success", "Room updated successfully!")
            self.accept()  # Close the dialog with success
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update room: {e}")
