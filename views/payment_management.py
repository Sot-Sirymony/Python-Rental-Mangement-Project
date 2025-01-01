
from PyQt6.QtWidgets import (
    QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QComboBox, QLineEdit, QMessageBox, QHeaderView, QDateEdit, QWidget
)
from PyQt6.QtCore import QDate
from functools import partial
from views.add_payment import AddPaymentView
from views.edit_payment import EditPaymentDialog
from controllers.payment_controller import fetch_payment_history, delete_payment, fetch_payment_methods, fetch_payment_statuses


class PaymentManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Payment Management")
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Payment Management"))

        # Search Input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Tenant, Room, or Reference")
        self.search_input.textChanged.connect(self.filter_payments)
        self.layout.addWidget(self.search_input)

        # Filter: Payment Method
        self.filter_method = QComboBox()
        self.filter_method.addItem("All Methods")
        self.populate_payment_methods()  # Dynamically load methods
        self.filter_method.currentTextChanged.connect(self.filter_payments)
        self.layout.addWidget(self.filter_method)

        # Filter: Payment Status
        self.filter_status = QComboBox()
        self.filter_status.addItem("All Statuses")
        self.populate_payment_statuses()  # Dynamically load statuses
        self.filter_status.currentTextChanged.connect(self.filter_payments)
        self.layout.addWidget(self.filter_status)

        # Date Range Filters
        self.start_date_filter = QDateEdit()
        self.start_date_filter.setCalendarPopup(True)
        self.start_date_filter.setDisplayFormat("yyyy-MM-dd")
        self.start_date_filter.setDate(QDate.currentDate().addMonths(-1))  # Default to last month
        self.start_date_filter.dateChanged.connect(self.filter_payments)
        self.layout.addWidget(self.start_date_filter)

        self.end_date_filter = QDateEdit()
        self.end_date_filter.setCalendarPopup(True)
        self.end_date_filter.setDisplayFormat("yyyy-MM-dd")
        self.end_date_filter.setDate(QDate.currentDate())  # Default to today
        self.end_date_filter.dateChanged.connect(self.filter_payments)
        self.layout.addWidget(self.end_date_filter)

        # Payment Table
        self.payment_table = QTableWidget()
        self.payment_table.setColumnCount(11)  # Added Notes column
        self.payment_table.setHorizontalHeaderLabels(
            ["ID", "Tenant", "Room", "Amount", "Method", "Date", "Due Date", "Status", "Reference", "Notes", "Actions"]
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

    def populate_payment_methods(self):
        """Dynamically populate the Payment Method filter."""
        try:
            methods = fetch_payment_methods()
            for method in methods:
                self.filter_method.addItem(method)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load payment methods: {e}")

    def populate_payment_statuses(self):
        """Dynamically populate the Payment Status filter."""
        try:
            statuses = fetch_payment_statuses()
            for status in statuses:
                self.filter_status.addItem(status)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load payment statuses: {e}")

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

        if not payments:
            self.payment_table.setRowCount(1)
            self.payment_table.setItem(0, 0, QTableWidgetItem("No payments found."))
            return

        for payment in payments:
            row = self.payment_table.rowCount()
            self.payment_table.insertRow(row)

            # Populate data columns (excluding the Actions column)
            for col, data in enumerate(payment):  # Include Notes column
                self.payment_table.setItem(row, col, QTableWidgetItem(str(data)))

            # Add Action buttons
            self.add_action_buttons(row, payment)

    def add_action_buttons(self, row, payment):
        """Add action buttons (Edit, Delete) to the Actions column."""
        actions_widget = QWidget()
        actions_layout = QVBoxLayout()
        actions_layout.setContentsMargins(0, 0, 0, 0)

        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setToolTip("Edit this payment")
        edit_btn.clicked.connect(partial(self.open_edit_payment_view, payment))
        actions_layout.addWidget(edit_btn)

        # Delete button
        delete_btn = QPushButton("Delete")
        delete_btn.setToolTip("Delete this payment")
        delete_btn.clicked.connect(partial(self.delete_payment_action, payment[0]))
        actions_layout.addWidget(delete_btn)

        actions_widget.setLayout(actions_layout)
        self.payment_table.setCellWidget(row, 10, actions_widget)

    def filter_payments(self):
        """Filter payments based on search and filter criteria."""
        search_text = self.search_input.text().lower()
        method_filter = self.filter_method.currentText()
        status_filter = self.filter_status.currentText()
        start_date = self.start_date_filter.date().toString("yyyy-MM-dd")
        end_date = self.end_date_filter.date().toString("yyyy-MM-dd")

        try:
            payments = fetch_payment_history(
                method=method_filter if method_filter != "All Methods" else None,
                start_date=start_date,
                end_date=end_date
            )
            filtered_payments = [
                payment for payment in payments
                if search_text in str(payment).lower() and
                   (status_filter == "All Statuses" or payment[7] == status_filter)
            ]
            self.populate_table(filtered_payments)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to filter payments: {e}")

    def open_add_payment_view(self):
        """Open the Add Payment view."""
        dialog = AddPaymentView(parent=self)
        if dialog.exec():
            self.load_payments()  # Refresh the table after adding a payment

    def open_edit_payment_view(self, payment):
        """Open the Edit Payment view."""
        dialog = EditPaymentDialog(payment, parent=self)
        if dialog.exec():
            self.load_payments()  # Refresh the table after editing a payment

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


