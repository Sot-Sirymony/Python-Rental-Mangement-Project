from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QFormLayout, QDateEdit, QComboBox

class PaymentManagement(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Payment Management"))

        # Record Payment Button
        record_payment_btn = QPushButton("Record Payment")
        record_payment_btn.clicked.connect(self.record_payment_form)
        layout.addWidget(record_payment_btn)

        # Payment History Table
        self.payment_table = QTableWidget(0, 5)  # Columns: Tenant, Room, Amount, Date, Method
        self.payment_table.setHorizontalHeaderLabels(["Tenant", "Room", "Amount", "Date", "Method"])
        layout.addWidget(self.payment_table)

        self.setLayout(layout)

    def record_payment_form(self):
        form = QWidget()
        form_layout = QFormLayout()

        tenant_input = QLineEdit()
        room_input = QLineEdit()
        amount_input = QLineEdit()
        date_input = QDateEdit()
        method_input = QComboBox()
        method_input.addItems(["Cash", "Bank Transfer", "Check"])

        form_layout.addRow("Tenant", tenant_input)
        form_layout.addRow("Room", room_input)
        form_layout.addRow("Amount", amount_input)
        form_layout.addRow("Date", date_input)
        form_layout.addRow("Method", method_input)

        save_btn = QPushButton("Save Payment")
        save_btn.clicked.connect(lambda: self.save_payment(tenant_input.text(), room_input.text(), amount_input.text(), date_input.text(), method_input.currentText()))
        form_layout.addWidget(save_btn)

        form.setLayout(form_layout)
        form.show()

    def save_payment(self, tenant, room, amount, date, method):
        from controllers.payment_controller import add_payment
        add_payment(tenant, room, amount, date, method)
        self.refresh_payment_table()

    def refresh_payment_table(self):
        from controllers.payment_controller import get_all_payments
        payments = get_all_payments()
        self.payment_table.setRowCount(0)  # Clear table
        for payment in payments:
            row = self.payment_table.rowCount()
            self.payment_table.insertRow(row)
            self.payment_table.setItem(row, 0, QTableWidgetItem(payment['tenant']))
            self.payment_table.setItem(row, 1, QTableWidgetItem(payment['room']))
            self.payment_table.setItem(row, 2, QTableWidgetItem(str(payment['amount'])))
            self.payment_table.setItem(row, 3, QTableWidgetItem(payment['date']))
            self.payment_table.setItem(row, 4, QTableWidgetItem(payment['method']))
