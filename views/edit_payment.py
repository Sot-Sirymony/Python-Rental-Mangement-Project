
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QDateEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import QDate
from controllers.payment_controller import update_payment  # Ensure this function supports the updated schema

class EditPaymentDialog(QDialog):
    def __init__(self, payment_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Payment")
        self.layout = QVBoxLayout()

        self.payment_id = payment_data[0]
        tenant_name = payment_data[1]
        room_name = payment_data[2]
        # Pre-fill fields with existing data
        self.layout.addWidget(QLabel(f"Editing Payment for {tenant_name} in Room {room_name}"))
        # Payment Amount
        self.layout.addWidget(QLabel("Payment Amount"))
        self.amount_input = QLineEdit(str(payment_data[3]))
        self.amount_input.setPlaceholderText("Enter payment amount")
        self.layout.addWidget(self.amount_input)

        # Payment Method
        self.layout.addWidget(QLabel("Payment Method"))
        self.method_input = QComboBox()
        self.method_input.addItems(["Cash", "Bank Transfer", "Check"])
        self.method_input.setCurrentText(payment_data[4])
        self.layout.addWidget(self.method_input)

        # Payment Date
        self.layout.addWidget(QLabel("Payment Date"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setDate(QDate.fromString(payment_data[5], "yyyy-MM-dd"))
        self.layout.addWidget(self.date_input)

        # Due Date
        self.layout.addWidget(QLabel("Due Date"))
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDisplayFormat("yyyy-MM-dd")
        self.due_date_input.setDate(
            QDate.fromString(payment_data[7], "yyyy-MM-dd") if payment_data[7] else QDate.currentDate()
        )
        self.layout.addWidget(self.due_date_input)

        # Payment Reference
        self.layout.addWidget(QLabel("Payment Reference (Optional)"))
        self.reference_input = QLineEdit(payment_data[8])
        self.reference_input.setPlaceholderText("Enter reference (if any)")
        self.layout.addWidget(self.reference_input)

        # Payment Status
        self.layout.addWidget(QLabel("Payment Status"))
        self.status_selector = QComboBox()
        self.status_selector.addItems(["Pending", "Paid", "Overdue"])
        self.status_selector.setCurrentText(payment_data[9])
        self.layout.addWidget(self.status_selector)

        # Save Changes Button
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.save_payment)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

    def save_payment(self):
        amount = self.amount_input.text().strip()
        method = self.method_input.currentText()
        payment_date = self.date_input.date().toString("yyyy-MM-dd")
        due_date = self.due_date_input.date().toString("yyyy-MM-dd")
        reference = self.reference_input.text().strip()
        payment_status = self.status_selector.currentText()

        # Validate inputs
        if not amount or not amount.replace(".", "", 1).isdigit() or float(amount) <= 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid payment amount (positive number).")
            self.amount_input.setFocus()
            return

        if due_date < payment_date:
            QMessageBox.warning(self, "Validation Error", "Due date must not be earlier than payment date.")
            self.due_date_input.setFocus()
            return

        if not method:
            QMessageBox.warning(self, "Validation Error", "Please select a payment method.")
            self.method_input.setFocus()
            return

        if not payment_status:
            QMessageBox.warning(self, "Validation Error", "Please select a payment status.")
            self.status_selector.setFocus()
            return

        try:
            # Update payment using the controller
            update_payment(self.payment_id, float(amount), method, payment_date, due_date, reference, payment_status)
            QMessageBox.information(self, "Success", "Payment updated successfully!")
            self.accept()
        except Exception as e:
            print(f"Error updating payment: {e}")
            QMessageBox.critical(self, "Error", f"Failed to update payment: {e}")


