
from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QLabel, QWidget
from controllers.room_controller import add_room

class AddRoomView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Room")
        self.layout = QVBoxLayout()

        # Error Label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.layout.addWidget(self.error_label)

        # Room Name
        self.name_label = QLabel("Room Name/Number:")
        self.layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Room Name/Number")
        self.layout.addWidget(self.name_input)

        # Room Type
        self.type_label = QLabel("Room Type:")
        self.layout.addWidget(self.type_label)
        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("Enter Room Type (e.g., Single, Double)")
        self.layout.addWidget(self.type_input)

        # Room Size
        self.size_label = QLabel("Room Size (e.g., sq ft or m²):")
        self.layout.addWidget(self.size_label)
        self.size_input = QLineEdit()
        self.size_input.setPlaceholderText("Enter Size (e.g., 25.5)")
        self.layout.addWidget(self.size_input)

        # Rental Price
        self.price_label = QLabel("Rental Price:")
        self.layout.addWidget(self.price_label)
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Enter Rental Price")
        self.layout.addWidget(self.price_input)

        # Amenities
        self.amenities_label = QLabel("Amenities:")
        self.layout.addWidget(self.amenities_label)
        self.amenities_input = QLineEdit()
        self.amenities_input.setPlaceholderText("Enter Amenities (comma-separated)")
        self.layout.addWidget(self.amenities_input)

        # Save Room Button
        self.add_btn = QPushButton("Save Room")
        self.add_btn.clicked.connect(self.save_room)
        self.layout.addWidget(self.add_btn)

        self.setLayout(self.layout)

    def save_room(self):
        # Get input values
        name = self.name_input.text().strip()
        room_type = self.type_input.text().strip()
        size = self.size_input.text().strip()
        rental_price = self.price_input.text().strip()
        amenities = self.amenities_input.text().strip()

        # Validation
        if not name:
            self.error_label.setText("Error: Room Name/Number is required.")
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
            # Convert numeric fields
            size = float(size)
            rental_price = float(rental_price)

            # Save room data
            add_room(name, room_type, size, rental_price, amenities)
            print("Room added successfully!")
            self.close()
        except Exception as e:
            self.error_label.setText(f"Error: Failed to add room. {e}")
