from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QDateEdit, QTextEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import QDate
from controllers.payment_controller import add_payment, fetch_payment_methods, fetch_payment_statuses

class AddPaymentView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Payment")
        self.resize(400, 400)
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
        self.populate_payment_methods()  # Dynamically load methods
        self.layout.addWidget(self.method_selector)

        # Payment Date
        self.layout.addWidget(QLabel("Payment Date"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setDate(QDate.currentDate())  # Default to current date
        self.layout.addWidget(self.date_input)

        # Due Date (Optional)
        self.layout.addWidget(QLabel("Due Date (Optional)"))
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDisplayFormat("yyyy-MM-dd")
        self.layout.addWidget(self.due_date_input)

        # Payment Reference (Optional)
        self.layout.addWidget(QLabel("Payment Reference (Optional)"))
        self.reference_input = QTextEdit()
        self.reference_input.setPlaceholderText("Enter reference if any")
        self.layout.addWidget(self.reference_input)

        # Payment Status
        self.layout.addWidget(QLabel("Payment Status"))
        self.status_selector = QComboBox()
        self.populate_payment_statuses()  # Dynamically load statuses
        self.layout.addWidget(self.status_selector)

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
        from controllers.room_controller import fetch_available_rooms
        rooms = fetch_available_rooms()
        if rooms:
            for room in rooms:
                self.room_selector.addItem(f"{room[1]} ({room[0]})", room[0])  # Display room name/ID, store room_id
        else:
            self.room_selector.addItem("No rooms found", None)

    def populate_payment_methods(self):
        """Dynamically load payment methods."""
        methods = fetch_payment_methods()
        if methods:
            self.method_selector.addItems(methods)
        else:
            self.method_selector.addItem("No methods available")

    def populate_payment_statuses(self):
        """Dynamically load payment statuses."""
        statuses = fetch_payment_statuses()
        if statuses:
            self.status_selector.addItems(statuses)
        else:
            self.status_selector.addItem("No statuses available")

    def save_payment(self):
        """Save the payment data to the database."""
        tenant_id = self.tenant_selector.currentData()
        room_id = self.room_selector.currentData()
        amount = self.amount_input.text().strip()
        method = self.method_selector.currentText()
        date = self.date_input.date().toString("yyyy-MM-dd")
        due_date = self.due_date_input.date().toString("yyyy-MM-dd") if self.due_date_input.date() else None
        reference = self.reference_input.toPlainText().strip()
        status = self.status_selector.currentText()

        # Validation
        if not tenant_id:
            QMessageBox.warning(self, "Validation Error", "Please select a tenant.")
            return
        if not room_id:
            QMessageBox.warning(self, "Validation Error", "Please select a room.")
            return
        if not amount or not amount.replace(".", "", 1).isdigit() or float(amount) <= 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid payment amount (positive number).")
            return
        if due_date and due_date < date:
            QMessageBox.warning(self, "Validation Error", "Due date must not be earlier than payment date.")
            return

        try:
            # Save payment using the controller
            add_payment(tenant_id, room_id, float(amount), date, method, reference, due_date, status)
            QMessageBox.information(self, "Success", "Payment added successfully!")
            if self.parent():
                self.parent().load_payments()  # Refresh parent view
            self.accept()  # Close the dialog
        except Exception as e:
            print(f"Error adding payment: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add payment: {e}")
