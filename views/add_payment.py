

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDateEdit, QLineEdit, QPushButton, QDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from controllers.payment_management_controller import create_payment, fetch_available_rooms, fetch_tenants


class AddPaymentView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Payment")
        self.layout = QVBoxLayout()

        # Tenant Selection
        tenant_label = QLabel("Select Tenant:")
        tenant_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(tenant_label)

        self.tenant_selector = QComboBox()
        self.tenant_selector.setStyleSheet("font-size: 14px;")
        self.load_tenants()
        self.layout.addWidget(self.tenant_selector)

        # Room Selection
        room_label = QLabel("Select Room:")
        room_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(room_label)

        self.room_selector = QComboBox()
        self.room_selector.setStyleSheet("font-size: 14px;")
        self.load_rooms()
        self.layout.addWidget(self.room_selector)

        # Amount
        amount_label = QLabel("Amount:")
        amount_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(amount_label)

        self.amount_input = QLineEdit()
        self.amount_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.amount_input)

        # Payment Date
        payment_date_label = QLabel("Payment Date:")
        payment_date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(payment_date_label)

        self.payment_date_input = QDateEdit()
        self.payment_date_input.setCalendarPopup(True)
        self.payment_date_input.setDate(QDate.currentDate())
        self.payment_date_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.payment_date_input)

        # Due Date
        due_date_label = QLabel("Due Date:")
        due_date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(due_date_label)

        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.due_date_input)

        # Method
        method_label = QLabel("Payment Method:")
        method_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(method_label)

        self.method_input = QComboBox()
        self.method_input.addItems(["Cash", "Bank Transfer", "Check"])
        self.method_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.method_input)

        # Reference Number
        reference_label = QLabel("Reference Number:")
        reference_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(reference_label)

        self.reference_input = QLineEdit()
        self.reference_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.reference_input)

        # Notes
        notes_label = QLabel("Notes:")
        notes_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(notes_label)

        self.notes_input = QLineEdit()
        self.notes_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.notes_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Payment")
        self.save_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 6px;")
        self.save_btn.clicked.connect(self.save_payment)
        button_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 6px;")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def load_rooms(self):
        """Load available rooms into the dropdown."""
        try:
            rooms = fetch_available_rooms()
            for room in rooms:
                self.room_selector.addItem(f"{room[1]} (ID: {room[0]})", room[0])  # Display name, store ID
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load rooms: {e}")

    def load_tenants(self):
        """Load tenants into the dropdown."""
        try:
            tenants = fetch_tenants()
            for tenant in tenants:
                self.tenant_selector.addItem(f"{tenant[1]} (ID: {tenant[0]})", tenant[0])  # Display name, store ID
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load tenants: {e}")

    def save_payment(self):
        """Save the payment."""
        tenant_id = self.tenant_selector.currentData()
        room_id = self.room_selector.currentData()
        amount = self.amount_input.text()
        date = self.payment_date_input.date().toString("yyyy-MM-dd")
        due_date = self.due_date_input.date().toString("yyyy-MM-dd")
        method = self.method_input.currentText()
        reference = self.reference_input.text()
        notes = self.notes_input.text()

        if not tenant_id or not room_id or not amount:
            QMessageBox.warning(self, "Validation Error", "All fields are required.")
            return

        try:
            create_payment(tenant_id, room_id, float(amount), date, due_date, method, reference, notes)
            QMessageBox.information(self, "Success", "Payment recorded successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to record payment: {e}")


