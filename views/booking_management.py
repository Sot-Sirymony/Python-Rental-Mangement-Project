

from PyQt6.QtWidgets import (
    QVBoxLayout, QPushButton, QLabel, QInputDialog, QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
)
from functools import partial
from controllers.booking_controller import fetch_bookings, cancel_booking, confirm_booking, delete_booking  # Import delete_booking function
from views.add_booking import AddBookingView
from views.edit_booking import EditBookingView

class BookingManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Booking Management"))

        # Booking Table
        self.booking_table = QTableWidget()
        self.booking_table.setColumnCount(11)  # Include Notes column
        self.booking_table.setHorizontalHeaderLabels(
            ["ID", "Room", "Tenant", "Start Date", "End Date", "Status", "Notes", "Edit", "Cancel", "Confirm", "Delete"]
        )
        self.booking_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.booking_table)

        # Add and Refresh Buttons
        self.add_booking_btn = QPushButton("Add New Booking")
        self.add_booking_btn.clicked.connect(self.open_add_booking_view)
        self.layout.addWidget(self.add_booking_btn)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load_bookings)
        self.layout.addWidget(self.refresh_btn)

        self.setLayout(self.layout)
        self.load_bookings()

    def load_bookings(self):
        try:
            bookings = fetch_bookings()
            print("Fetched bookings:", bookings)  # Debug: Print fetched bookings
            self.booking_table.setRowCount(0)

            if not bookings:
                QMessageBox.information(self, "Info", "No bookings found.")
                return

            for row_data in bookings:
                print("Processing row:", row_data)  # Debug: Print each row data
                row = self.booking_table.rowCount()
                self.booking_table.insertRow(row)

                # Populate data columns
                for col, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    self.booking_table.setItem(row, col, item)

                # Add Edit button
                edit_btn = QPushButton("Edit")
                edit_btn.clicked.connect(partial(self.open_edit_booking_view, row_data))
                self.booking_table.setCellWidget(row, 7, edit_btn)

                # Add Cancel button
                cancel_btn = QPushButton("Cancel")
                if row_data[5] != "Canceled":
                    cancel_btn.clicked.connect(partial(self.cancel_booking_action, row_data[0]))
                self.booking_table.setCellWidget(row, 8, cancel_btn)

                # Add Confirm button
                confirm_btn = QPushButton("Confirm")
                if row_data[5] == "Pending":
                    confirm_btn.clicked.connect(partial(self.confirm_booking_action, row_data[0]))
                self.booking_table.setCellWidget(row, 9, confirm_btn)

                # Add Delete button
                delete_btn = QPushButton("Delete")
                delete_btn.clicked.connect(partial(self.delete_booking_action, row_data[0]))
                self.booking_table.setCellWidget(row, 10, delete_btn)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load bookings: {e}")     
            
    def open_add_booking_view(self):
        try:
            self.add_booking_view = AddBookingView(parent=self)
            self.add_booking_view.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open Add Booking View: {e}")
    def open_edit_booking_view(self, booking_data):
        try:
            print("Opening Edit Booking View with data:", booking_data)  # Debug
            self.edit_booking_view = EditBookingView(booking_data, parent=self)
            self.edit_booking_view.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open Edit Booking View: {e}")


    def cancel_booking_action(self, booking_id):
        reason, ok = QInputDialog.getText(self, "Cancel Booking", "Provide a reason for cancellation:")
        if ok and reason.strip():
            try:
                cancel_booking(booking_id, reason)
                QMessageBox.information(self, "Success", "Booking canceled successfully!")
                self.load_bookings()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to cancel booking: {e}")

    def confirm_booking_action(self, booking_id):
        try:
            confirm_booking(booking_id)
            QMessageBox.information(self, "Success", "Booking confirmed successfully!")
            self.load_bookings()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to confirm booking: {e}")

    def delete_booking_action(self, booking_id):
        confirmation = QMessageBox.question(
            self,
            "Delete Booking",
            "Are you sure you want to delete this booking?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            try:
                delete_booking(booking_id)
                QMessageBox.information(self, "Success", "Booking deleted successfully!")
                self.load_bookings()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete booking: {e}")
