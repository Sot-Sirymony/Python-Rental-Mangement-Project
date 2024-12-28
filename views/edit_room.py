
from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QLabel, QWidget
from controllers.property_controller import update_room

class EditRoomView(QWidget):
    def __init__(self, room_id, current_data):
        super().__init__()
        self.setWindowTitle("Edit Room")
        self.room_id = room_id
        self.layout = QVBoxLayout()

        # Error Label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.layout.addWidget(self.error_label)

        # Room Name
        self.name_label = QLabel("Room Name:")
        self.layout.addWidget(self.name_label)
        self.name_input = QLineEdit(current_data['name'])
        self.name_input.setPlaceholderText("Enter Room Name")
        self.layout.addWidget(self.name_input)

        # Room Type
        self.type_label = QLabel("Room Type:")
        self.layout.addWidget(self.type_label)
        self.type_input = QLineEdit(current_data['type'])
        self.type_input.setPlaceholderText("Enter Room Type (e.g., Single, Double)")
        self.layout.addWidget(self.type_input)

        # Room Size
        self.size_label = QLabel("Room Size:")
        self.layout.addWidget(self.size_label)
        self.size_input = QLineEdit(current_data['size'])
        self.size_input.setPlaceholderText("Enter Room Size (e.g., 25.5 sqm)")
        self.layout.addWidget(self.size_input)

        # Rental Price
        self.price_label = QLabel("Rental Price:")
        self.layout.addWidget(self.price_label)
        self.price_input = QLineEdit(current_data['rental_price'])
        self.price_input.setPlaceholderText("Enter Rental Price")
        self.layout.addWidget(self.price_input)

        # Amenities
        self.amenities_label = QLabel("Amenities:")
        self.layout.addWidget(self.amenities_label)
        self.amenities_input = QLineEdit(current_data['amenities'])
        self.amenities_input.setPlaceholderText("Enter Amenities (comma-separated)")
        self.layout.addWidget(self.amenities_input)

        # Save Changes Button
        self.update_btn = QPushButton("Save Changes")
        self.update_btn.clicked.connect(self.save_changes)
        self.layout.addWidget(self.update_btn)

        self.setLayout(self.layout)

    def save_changes(self):
        # Fetch input values
        name = self.name_input.text().strip()
        room_type = self.type_input.text().strip()
        size = self.size_input.text().strip()
        rental_price = self.price_input.text().strip()
        amenities = self.amenities_input.text().strip()

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
            update_room(self.room_id, name, room_type, size, rental_price, amenities)
            print("Room updated successfully!")
            self.close()
        except Exception as e:
            self.error_label.setText(f"Error: Failed to update room. {e}")

