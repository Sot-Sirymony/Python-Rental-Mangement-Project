from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QDateEdit, QTextEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import QDate
from controllers.payment_controller import add_payment  # Import your add_payment function from the controller

class AddPaymentView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Payment")
        self.resize(400, 300)
        self.setModal(True)  # Make the dialog modal

        self.layout = QVBoxLayout()

        # Tenant Selector
        self.layout.addWidget(QLabel("Select Tenant"))
        self.tenant_selector = QComboBox()
        self.load_tenants()  # Populate tenant dropdown
        self.layout.addWidget(self.tenant_selector)

        # Room Selector
        self.layout.addWidget(QLabel("Select Room"))
        self.room_selector = QComboBox()
        self.load_rooms()  # Populate room dropdown
        self.layout.addWidget(self.room_selector)

        # Payment Amount
        self.layout.addWidget(QLabel("Payment Amount"))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter payment amount")
        self.layout.addWidget(self.amount_input)

        # Payment Method
        self.layout.addWidget(QLabel("Payment Method"))
        self.method_selector = QComboBox()
        self.method_selector.addItems(["Cash", "Bank Transfer", "Check"])  # Populate payment methods
        self.layout.addWidget(self.method_selector)

        # Payment Date
        self.layout.addWidget(QLabel("Payment Date"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setDate(QDate.currentDate())  # Default to current date
        self.layout.addWidget(self.date_input)

        # Payment Reference
        self.layout.addWidget(QLabel("Payment Reference (Optional)"))
        self.reference_input = QTextEdit()
        self.layout.addWidget(self.reference_input)

        # Save Button
        self.save_btn = QPushButton("Save Payment")
        self.save_btn.clicked.connect(self.save_payment)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

    def load_tenants(self):
        """Load tenants into the tenant dropdown."""
        from controllers.tenant_controller import fetch_tenants
        tenants = fetch_tenants()
        if tenants:
            for tenant in tenants:
                self.tenant_selector.addItem(f"{tenant[1]} {tenant[2]}", tenant[0])  # Display full name, store tenant_id
        else:
            self.tenant_selector.addItem("No tenants found", None)

    def load_rooms(self):
        """Load rooms into the room dropdown."""
        from controllers.property_controller import fetch_properties
        rooms = fetch_properties()
        if rooms:
            for room in rooms:
                self.room_selector.addItem(f"{room[1]} ({room[0]})", room[0])  # Display room name/ID, store room_id
        else:
            self.room_selector.addItem("No rooms found", None)

    def save_payment(self):
        """Save the payment data to the database."""
        tenant_id = self.tenant_selector.currentData()
        room_id = self.room_selector.currentData()
        amount = self.amount_input.text().strip()
        method = self.method_selector.currentText()
        date = self.date_input.date().toString("yyyy-MM-dd")
        reference = self.reference_input.toPlainText().strip()

        # Validation
        if not tenant_id:
            QMessageBox.warning(self, "Validation Error", "Please select a tenant.")
            return
        if not room_id:
            QMessageBox.warning(self, "Validation Error", "Please select a room.")
            return
        if not amount or not amount.replace(".", "").isdigit():
            QMessageBox.warning(self, "Validation Error", "Please enter a valid payment amount.")
            return

        try:
            # Save payment using the controller
            add_payment(tenant_id, room_id, float(amount), method, date, reference)
            QMessageBox.information(self, "Success", "Payment added successfully!")
            if self.parent():
                self.parent().load_payments()  # Refresh parent view
            self.accept()  # Close the dialog
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add payment: {e}")
