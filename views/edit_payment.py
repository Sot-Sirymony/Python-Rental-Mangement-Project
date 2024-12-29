from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox,QLineEdit, QDateEdit, QTextEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import QDate
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

        self.amount_input = QLineEdit(str(payment_data[3]))
        self.layout.addWidget(self.amount_input)

        self.method_input = QComboBox()
        self.method_input.addItems(["Cash", "Bank Transfer", "Check"])
        self.method_input.setCurrentText(payment_data[4])
        self.layout.addWidget(self.method_input)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setDate(QDate.fromString(payment_data[5], "yyyy-MM-dd"))
        self.layout.addWidget(self.date_input)

        self.reference_input = QLineEdit(payment_data[6])
        self.layout.addWidget(self.reference_input)

        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.save_payment)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

    def save_payment(self):
        amount = self.amount_input.text()
        method = self.method_input.currentText()
        payment_date = self.date_input.date().toString("yyyy-MM-dd")
        reference = self.reference_input.text()

        # Assume tenant_id and room_id are retrievable or part of the dialog
        tenant_id = 1  # Replace with actual tenant_id
        room_id = 1  # Replace with actual room_id

        try:
            update_payment(self.payment_id, tenant_id, room_id, amount, method, payment_date, reference)
            QMessageBox.information(self, "Success", "Payment updated successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update payment: {e}")
