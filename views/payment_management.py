

from PyQt6.QtWidgets import (
    QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox,
    QWidget, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from controllers.payment_management_controller import fetch_payments, create_payment, update_payment, delete_payment
from views.add_payment import AddPaymentView
from views.edit_payment import EditPaymentView


class PaymentManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Payment Management")
        self.layout = QVBoxLayout()

        # Payment Table
        self.payment_table = QTableWidget()
        self.payment_table.setColumnCount(10)  # Columns for payment details and actions
        self.payment_table.setHorizontalHeaderLabels([
            "Payment ID", "Room Name", "Tenant Name", "Amount", "Payment Date",
            "Due Date", "Method", "Status", "Edit", "Delete"
        ])

        # Table styling
        self.payment_table.setStyleSheet("""
            QTableWidget::item { font-size: 14px; text-align: center; }
            QHeaderView::section { font-size: 16px; font-weight: bold; text-align: center; }
        """)
        self.payment_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.payment_table)

        # Refresh Button
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 8px;")
        self.refresh_btn.clicked.connect(self.load_payments)
        self.layout.addWidget(self.refresh_btn)

        # Add Payment Button
        self.add_payment_btn = QPushButton("Add Payment")
        self.add_payment_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 8px;")
        self.add_payment_btn.clicked.connect(self.open_add_payment_view)
        self.layout.addWidget(self.add_payment_btn)

        self.setLayout(self.layout)
        self.load_payments()

    def load_payments(self):
        """Load and display payments."""
        payments = fetch_payments()
        self.payment_table.setRowCount(0)

        for payment in payments:
            row = self.payment_table.rowCount()
            self.payment_table.insertRow(row)

            # Populate the table with payment data
            for col, data in enumerate(payment[:8]):  # Exclude actions for now
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.payment_table.setItem(row, col, item)

            # Edit Button
            edit_btn = QPushButton("Edit")
            edit_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 4px;")
            edit_btn.clicked.connect(lambda _, p=payment: self.edit_payment(p))
            self.payment_table.setCellWidget(row, 8, edit_btn)

            # Delete Button
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 4px;")
            delete_btn.clicked.connect(lambda _, p=payment: self.delete_payment_action(p[0]))
            self.payment_table.setCellWidget(row, 9, delete_btn)

    def edit_payment(self, payment):
        """Open Edit Payment dialog."""
        dialog = EditPaymentView(payment, self)
        if dialog.exec():
            self.load_payments()

    def delete_payment_action(self, payment_id):
        """Delete a payment with confirmation."""
        reply = QMessageBox.question(
            self, "Delete Payment",
            f"Are you sure you want to delete payment ID {payment_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_payment(payment_id)
                QMessageBox.information(self, "Success", f"Payment {payment_id} deleted successfully!")
                self.load_payments()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete payment: {e}")

    def open_add_payment_view(self):
        """Open Add Payment dialog."""
        dialog = AddPaymentView(self)
        if dialog.exec():
            self.load_payments()

