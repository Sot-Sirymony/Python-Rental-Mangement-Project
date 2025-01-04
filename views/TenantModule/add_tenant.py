

from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QLabel, QDialog
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator

class AddTenantView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Tenant")
        self.layout = QVBoxLayout()

        # Set dialog styles
        self.setStyleSheet("""
            QLabel { font-size: 16px; }
            QLineEdit { font-size: 14px; }
        """)

        # Error Label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.layout.addWidget(self.error_label)

        # First Name
        self.first_name_label = QLabel("First Name:")
        self.layout.addWidget(self.first_name_label)
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Enter First Name")
        self.first_name_input.setStyleSheet("font-size: 14px;")  # Placeholder and value font size
        self.layout.addWidget(self.first_name_input)

        # Last Name
        self.last_name_label = QLabel("Last Name:")
        self.layout.addWidget(self.last_name_label)
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Enter Last Name")
        self.last_name_input.setStyleSheet("font-size: 14px;")  # Placeholder and value font size
        self.layout.addWidget(self.last_name_input)

        # Phone
        self.phone_label = QLabel("Phone:")
        self.layout.addWidget(self.phone_label)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter Phone Number")
        self.phone_input.setValidator(QIntValidator())  # Accepts only numeric input
        self.phone_input.setStyleSheet("font-size: 14px;")  # Placeholder and value font size
        self.layout.addWidget(self.phone_input)

        # Email
        self.email_label = QLabel("Email:")
        self.layout.addWidget(self.email_label)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter Email Address")
        email_regex = QRegularExpression(r"^[\w\.-]+@[\w\.-]+\.\w+$")
        self.email_input.setValidator(QRegularExpressionValidator(email_regex))
        self.email_input.setStyleSheet("font-size: 14px;")  # Placeholder and value font size
        self.layout.addWidget(self.email_input)

        # Save Button
        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet("font-size: 14px; padding: 8px;")
        self.save_btn.clicked.connect(self.save_tenant)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

    def save_tenant(self):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()

        # Validation
        if not first_name:
            self.error_label.setText("Error: First Name is required.")
            return
        if not last_name:
            self.error_label.setText("Error: Last Name is required.")
            return
        if not phone:
            self.error_label.setText("Error: Phone number is required.")
            return
        if not email:
            self.error_label.setText("Error: Email is required.")
            return
        if not self.email_input.hasAcceptableInput():
            self.error_label.setText("Error: Enter a valid email address.")
            return

        # Call the controller to save the tenant
        from controllers.SqlLiteControllers.tenant_controller import add_tenant
        try:
            add_tenant(first_name, last_name, phone, email)
            print("Tenant added successfully!")
            self.accept()  # Close the dialog
        except Exception as e:
            self.error_label.setText(f"Error adding tenant: {e}")


