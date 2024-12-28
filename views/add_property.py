
from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel, QWidget
from controllers.property_controller import add_property

class AddPropertyView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Property")
        self.layout = QVBoxLayout()

        # Error Label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.layout.addWidget(self.error_label)

        # Property Name
        self.name_label = QLabel("Property Name:")
        self.layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Property Name")
        self.layout.addWidget(self.name_input)

        # Address
        self.address_label = QLabel("Address:")
        self.layout.addWidget(self.address_label)
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Enter Property Address")
        self.layout.addWidget(self.address_input)

        # Description
        self.description_label = QLabel("Description:")
        self.layout.addWidget(self.description_label)
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter Property Description")
        self.layout.addWidget(self.description_input)

        # Amenities
        self.amenities_label = QLabel("Amenities:")
        self.layout.addWidget(self.amenities_label)
        self.amenities_input = QLineEdit()
        self.amenities_input.setPlaceholderText("Enter Amenities (comma-separated)")
        self.layout.addWidget(self.amenities_input)

        # Save Button
        self.add_btn = QPushButton("Save Property")
        self.add_btn.clicked.connect(self.save_property)
        self.layout.addWidget(self.add_btn)

        self.setLayout(self.layout)

    def save_property(self):
        # Get input values
        name = self.name_input.text().strip()
        address = self.address_input.text().strip()
        description = self.description_input.toPlainText().strip()
        amenities = self.amenities_input.text().strip()

        # Input validation
        if not name:
            self.error_label.setText("Error: Property Name is required.")
            return
        if not address:
            self.error_label.setText("Error: Address is required.")
            return
        if not description:
            self.error_label.setText("Error: Description is required.")
            return

        try:
            # Call the add property function
            add_property(name, address, description, amenities)
            print("Property added successfully!")
            self.close()
        except Exception as e:
            self.error_label.setText(f"Error: Failed to add property. {e}")

