

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QComboBox, QTextEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import QDate
from controllers.lease_management_controller import create_lease

class CreateLeaseView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Lease")
        self.resize(400, 400)
        self.layout = QVBoxLayout()

        # Room Selector
        self.layout.addWidget(QLabel("Select Room:"))
        self.room_selector = QComboBox()
        self.populate_rooms()
        self.layout.addWidget(self.room_selector)

        # Tenant Selector
        self.layout.addWidget(QLabel("Select Tenant:"))
        self.tenant_selector = QComboBox()
        self.populate_tenants()
        self.layout.addWidget(self.tenant_selector)

        # Start Date
        self.layout.addWidget(QLabel("Start Date:"))
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        self.layout.addWidget(self.start_date)

        # End Date
        self.layout.addWidget(QLabel("End Date:"))
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate().addMonths(1))  # Default to 1 month later
        self.layout.addWidget(self.end_date)

        # Lease Notes
        self.layout.addWidget(QLabel("Lease Notes (Optional):"))
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Enter any special terms or notes for the lease")
        self.layout.addWidget(self.notes_input)

        # Save Button
        self.save_btn = QPushButton("Create Lease")
        self.save_btn.clicked.connect(self.create_lease)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

    def populate_rooms(self):
        from controllers.rental_management_controller import fetch_room_details
        rooms = fetch_room_details()
        for room in rooms:
            # Only show available rooms with no active bookings or leases
            if room[7] == "Available" and room[9] != "Pending" and room[9] != "Active":
                self.room_selector.addItem(f"{room[1]} (ID: {room[0]})", room[0])

    def populate_tenants(self):
        from controllers.tenant_controller import fetch_tenants
        tenants = fetch_tenants()
        for tenant in tenants:
            # Optionally exclude tenants with active leases
            self.tenant_selector.addItem(f"{tenant[1]} {tenant[2]} (ID: {tenant[0]})", tenant[0])

    def create_lease(self):
        room_id = self.room_selector.currentData()
        tenant_id = self.tenant_selector.currentData()
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        notes = self.notes_input.toPlainText().strip()

        # Validate inputs
        if not room_id or not tenant_id:
            QMessageBox.warning(self, "Input Error", "Please select a room and tenant.")
            return
        if self.start_date.date() >= self.end_date.date():
            QMessageBox.warning(self, "Input Error", "End date must be after start date.")
            return

        try:
            # Call controller to create lease
            create_lease(room_id, tenant_id, start_date, end_date, notes)
            QMessageBox.information(self, "Success", "Lease created successfully!")
            self.accept()  # Close the dialog
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create lease: {e}")


