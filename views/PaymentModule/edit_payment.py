

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QComboBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import QDate
from controllers.PostGreSqlControllers.payment_management_controller import update_payment


from PyQt6.QtCore import QDate

class EditPaymentView(QDialog):
    def __init__(self, payment, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Payment")
        self.payment = payment  # payment is a tuple containing the payment details
        self.layout = QVBoxLayout()

        # Payment ID (read-only)
        payment_id_label = QLabel(f"Editing Payment ID: {payment[0]}")
        payment_id_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(payment_id_label)

        # Tenant Name (read-only)
        tenant_label = QLabel("Tenant Name:")
        tenant_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(tenant_label)

        self.tenant_name_input = QLineEdit(payment[2])
        self.tenant_name_input.setReadOnly(True)
        self.tenant_name_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.tenant_name_input)

        # Room Name (read-only)
        room_label = QLabel("Room Name:")
        room_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(room_label)

        self.room_name_input = QLineEdit(payment[1])
        self.room_name_input.setReadOnly(True)
        self.room_name_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.room_name_input)

        # Amount
        amount_label = QLabel("Amount:")
        amount_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(amount_label)

        self.amount_input = QLineEdit(str(payment[3]))
        self.amount_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.amount_input)

        # Payment Date
        payment_date_label = QLabel("Payment Date:")
        payment_date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(payment_date_label)

        # Convert `datetime.date` to `QDate`
        self.payment_date_input = QDateEdit(QDate(payment[4].year, payment[4].month, payment[4].day))
        self.payment_date_input.setCalendarPopup(True)
        self.payment_date_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.payment_date_input)

        # Due Date
        due_date_label = QLabel("Due Date:")
        due_date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(due_date_label)

        # Convert `datetime.date` to `QDate`
        self.due_date_input = QDateEdit(QDate(payment[5].year, payment[5].month, payment[5].day))
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.due_date_input)

        # Payment Method
        method_label = QLabel("Payment Method:")
        method_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(method_label)

        self.method_input = QComboBox()
        self.method_input.addItems(["Cash", "Bank Transfer", "Check"])
        self.method_input.setCurrentText(payment[6])
        self.method_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.method_input)

        # Payment Status
        status_label = QLabel("Payment Status:")
        status_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(status_label)

        self.status_input = QComboBox()
        self.status_input.addItems(["Pending", "Paid", "Overdue"])
        self.status_input.setCurrentText(payment[7])
        self.status_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.status_input)

        # Reference Number
        reference_label = QLabel("Reference Number:")
        reference_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(reference_label)

        self.reference_input = QLineEdit(payment[8] if payment[8] else "")
        self.reference_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.reference_input)

        # Notes
        notes_label = QLabel("Notes:")
        notes_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(notes_label)

        self.notes_input = QLineEdit(payment[9] if payment[9] else "")
        self.notes_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.notes_input)

        # Buttons
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 6px;")
        self.save_btn.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 6px;")
        self.cancel_btn.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_btn)

        self.setLayout(self.layout)

    def save_changes(self):
        """Save changes to the payment."""
        payment_id = self.payment[0]
        amount = self.amount_input.text().strip()
        date = self.payment_date_input.date().toString("yyyy-MM-dd")
        due_date = self.due_date_input.date().toString("yyyy-MM-dd")
        method = self.method_input.currentText()
        status = self.status_input.currentText()
        reference = self.reference_input.text().strip()
        notes = self.notes_input.text().strip()

        # Validate input
        if not amount or float(amount) <= 0:
            QMessageBox.warning(self, "Validation Error", "Amount must be greater than zero.")
            return

        try:
            update_payment(payment_id, float(amount), date, due_date, method, reference, notes, status)
            QMessageBox.information(self, "Success", "Payment updated successfully!")
            self.accept()  # Close the dialog
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update payment: {e}")