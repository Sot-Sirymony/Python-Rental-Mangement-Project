

from PyQt6.QtWidgets import (
    QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QComboBox, QLineEdit, QMessageBox, QHeaderView, QWidget
)
from functools import partial
from views.add_payment import AddPaymentView
from controllers.payment_controller import fetch_payment_history, delete_payment


# class PaymentManagement(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Payment Management")
#         self.layout = QVBoxLayout()

#         self.layout.addWidget(QLabel("Payment Management"))

#         # Search and Filter Section
#         self.search_input = QLineEdit()
#         self.search_input.setPlaceholderText("Search by Tenant, Room, or Reference")
#         self.search_input.textChanged.connect(self.filter_payments)
#         self.layout.addWidget(self.search_input)

#         self.filter_method = QComboBox()
#         self.filter_method.addItem("All Methods")
#         self.filter_method.addItems(["Cash", "Bank Transfer", "Check"])
#         self.filter_method.currentTextChanged.connect(self.filter_payments)
#         self.layout.addWidget(self.filter_method)

#         # Payment Table
#         self.payment_table = QTableWidget()
#         self.payment_table.setColumnCount(7)  # Columns for payment details
#         self.payment_table.setHorizontalHeaderLabels(
#             ["ID", "Tenant", "Room", "Amount", "Method", "Date", "Actions"]
#         )
#         self.payment_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
#         self.layout.addWidget(self.payment_table)

#         # Add and Refresh Buttons
#         self.add_payment_btn = QPushButton("Add Payment")
#         self.add_payment_btn.clicked.connect(self.open_add_payment_view)
#         self.layout.addWidget(self.add_payment_btn)

#         self.refresh_btn = QPushButton("Refresh Payments")
#         self.refresh_btn.clicked.connect(self.load_payments)
#         self.layout.addWidget(self.refresh_btn)

#         self.setLayout(self.layout)
#         self.load_payments()

#     def load_payments(self):
#         """Load all payments into the payment table."""
#         try:
#             payments = fetch_payment_history()  # Fetch payments from the database
#             self.populate_table(payments)
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Failed to load payments: {e}")
    
#     def populate_table(self, payments):
#         """Populate the payment table with data."""
#         self.payment_table.setRowCount(0)  # Clear existing rows

#         for payment in payments:
#             row = self.payment_table.rowCount()
#             self.payment_table.insertRow(row)

#             # Populate data columns (excluding the Actions column)
#             for col, data in enumerate(payment[:6]):
#                 self.payment_table.setItem(row, col, QTableWidgetItem(str(data)))

#             # Create an Edit button
#             edit_btn = QPushButton("Edit")
#             edit_btn.clicked.connect(partial(self.open_edit_payment_view, payment))
#             self.payment_table.setCellWidget(row, 6, edit_btn)

#             # Create a Delete button
#             delete_btn = QPushButton("Delete")
#             delete_btn.clicked.connect(partial(self.delete_payment_action, payment[0]))
#             # Add both Edit and Delete buttons to the Actions column
#             action_layout = QVBoxLayout()
#             action_layout.addWidget(edit_btn)
#             action_layout.addWidget(delete_btn)
            
#             action_widget = QWidget()
#             action_widget.setLayout(action_layout)
#             self.payment_table.setCellWidget(row, 6, action_widget)


#     def filter_payments(self):
#         """Filter payments based on search and filter criteria."""
#         search_text = self.search_input.text().lower()
#         method_filter = self.filter_method.currentText()

#         payments = fetch_payment_history()  # Fetch all payments from the database
#         filtered_payments = [
#             payment for payment in payments
#             if search_text in str(payment).lower() and
#                (method_filter == "All Methods" or payment[4] == method_filter)
#         ]
#         self.populate_table(filtered_payments)

#     def open_add_payment_view(self):
#         """Open the Add Payment view."""
#         dialog = AddPaymentView(parent=self)
#         if dialog.exec():
#             self.load_payments()  # Refresh the table after adding a payment

#     def open_edit_payment_view(self, payment_data):
#         """Open the Edit Payment view."""
#         from views.edit_payment import EditPaymentView
#         dialog = EditPaymentView(payment_data, parent=self)
#         if dialog.exec():
#             self.load_payments()  # Refresh the table after editing a payment

#     def delete_payment_action(self, payment_id):
#         """Delete a payment record."""
#         confirmation = QMessageBox.question(
#             self,
#             "Delete Payment",
#             "Are you sure you want to delete this payment?",
#             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
#         )
#         if confirmation == QMessageBox.StandardButton.Yes:
#             try:
#                 delete_payment(payment_id)
#                 QMessageBox.information(self, "Success", "Payment deleted successfully!")
#                 self.load_payments()  # Refresh the table after deletion
#             except Exception as e:
#                 QMessageBox.critical(self, "Error", f"Failed to delete payment: {e}")



class PaymentManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Payment Management")
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Payment Management"))

        # Search and Filter Section
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Tenant, Room, or Reference")
        self.search_input.textChanged.connect(self.filter_payments)
        self.layout.addWidget(self.search_input)

        self.filter_method = QComboBox()
        self.filter_method.addItem("All Methods")
        self.filter_method.addItems(["Cash", "Bank Transfer", "Check"])
        self.filter_method.currentTextChanged.connect(self.filter_payments)
        self.layout.addWidget(self.filter_method)

        # Payment Table
        self.payment_table = QTableWidget()
        self.payment_table.setColumnCount(7)  # Columns for payment details
        self.payment_table.setHorizontalHeaderLabels(
            ["ID", "Tenant", "Room", "Amount", "Method", "Date", "Actions"]  # Only Actions column
        )
        self.payment_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.payment_table)

        # Add and Refresh Buttons
        self.add_payment_btn = QPushButton("Add Payment")
        self.add_payment_btn.clicked.connect(self.open_add_payment_view)
        self.layout.addWidget(self.add_payment_btn)

        self.refresh_btn = QPushButton("Refresh Payments")
        self.refresh_btn.clicked.connect(self.load_payments)
        self.layout.addWidget(self.refresh_btn)

        self.setLayout(self.layout)
        self.load_payments()

    def load_payments(self):
        """Load all payments into the payment table."""
        try:
            payments = fetch_payment_history()  # Fetch payments from the database
            self.populate_table(payments)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load payments: {e}")

    def populate_table(self, payments):
        """Populate the payment table with data."""
        self.payment_table.setRowCount(0)  # Clear existing rows

        for payment in payments:
            row = self.payment_table.rowCount()
            self.payment_table.insertRow(row)

            # Populate data columns (excluding the Actions column)
            for col, data in enumerate(payment[:6]):  # Assuming the first 6 columns are data
                self.payment_table.setItem(row, col, QTableWidgetItem(str(data)))

            # Add Delete button only in the Actions column
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(partial(self.delete_payment_action, payment[0]))

            # Create a widget to hold the button
            action_widget = QWidget()
            action_layout = QVBoxLayout()
            action_layout.addWidget(delete_btn)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_widget.setLayout(action_layout)

            # Add the action widget to the Actions column
            self.payment_table.setCellWidget(row, 6, action_widget)

    def filter_payments(self):
        """Filter payments based on search and filter criteria."""
        search_text = self.search_input.text().lower()
        method_filter = self.filter_method.currentText()

        payments = fetch_payment_history()  # Fetch all payments from the database
        filtered_payments = [
            payment for payment in payments
            if search_text in str(payment).lower() and
               (method_filter == "All Methods" or payment[4] == method_filter)
        ]
        self.populate_table(filtered_payments)

    def open_add_payment_view(self):
        """Open the Add Payment view."""
        dialog = AddPaymentView(parent=self)
        if dialog.exec():
            self.load_payments()  # Refresh the table after adding a payment

    def delete_payment_action(self, payment_id):
        """Delete a payment record."""
        confirmation = QMessageBox.question(
            self,
            "Delete Payment",
            "Are you sure you want to delete this payment?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            try:
                delete_payment(payment_id)
                QMessageBox.information(self, "Success", "Payment deleted successfully!")
                self.load_payments()  # Refresh the table after deletion
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete payment: {e}")

