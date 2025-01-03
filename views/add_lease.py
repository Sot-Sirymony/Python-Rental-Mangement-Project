
# from PyQt6.QtWidgets import (
#     QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDateEdit, QPushButton, QDialog, QMessageBox
# )
# from PyQt6.QtCore import Qt, QDate
# from controllers.lease_management_controller import create_lease, fetch_available_rooms, fetch_tenants


# class AddLeaseView(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Add New Lease")
#         self.layout = QVBoxLayout()

#         # Room Selection
#         self.layout.addWidget(QLabel("Select Room:"))
#         self.room_selector = QComboBox()
#         self.load_rooms()
#         self.layout.addWidget(self.room_selector)

#         # Tenant Selection
#         self.layout.addWidget(QLabel("Select Tenant:"))
#         self.tenant_selector = QComboBox()
#         self.load_tenants()
#         self.layout.addWidget(self.tenant_selector)

#         # Start Date
#         self.layout.addWidget(QLabel("Start Date:"))
#         self.start_date_input = QDateEdit()
#         self.start_date_input.setCalendarPopup(True)
#         self.start_date_input.setDate(QDate.currentDate())
#         self.layout.addWidget(self.start_date_input)

#         # End Date
#         self.layout.addWidget(QLabel("End Date:"))
#         self.end_date_input = QDateEdit()
#         self.end_date_input.setCalendarPopup(True)
#         self.end_date_input.setDate(QDate.currentDate().addDays(30))  # Default to 30 days later
#         self.layout.addWidget(self.end_date_input)

#         # Buttons
#         button_layout = QHBoxLayout()
#         self.save_btn = QPushButton("Save Lease")
#         self.save_btn.clicked.connect(self.save_lease)
#         button_layout.addWidget(self.save_btn)

#         self.cancel_btn = QPushButton("Cancel")
#         self.cancel_btn.clicked.connect(self.reject)
#         button_layout.addWidget(self.cancel_btn)

#         self.layout.addLayout(button_layout)
#         self.setLayout(self.layout)

#     def load_rooms(self):
#         """Load available rooms into the dropdown."""
#         try:
#             rooms = fetch_available_rooms()
#             for room in rooms:
#                 self.room_selector.addItem(f"{room[1]} (ID: {room[0]})", room[0])  # Display name, store ID
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Failed to load rooms: {e}")

#     def load_tenants(self):
#         """Load tenants into the dropdown."""
#         try:
#             tenants = fetch_tenants()
#             for tenant in tenants:
#                 self.tenant_selector.addItem(f"{tenant[1]} (ID: {tenant[0]})", tenant[0])  # Display name, store ID
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Failed to load tenants: {e}")

#     def save_lease(self):
#         """Save the new lease."""
#         room_id = self.room_selector.currentData()
#         tenant_id = self.tenant_selector.currentData()
#         start_date = self.start_date_input.date().toString("yyyy-MM-dd")
#         end_date = self.end_date_input.date().toString("yyyy-MM-dd")

#         if not room_id or not tenant_id:
#             QMessageBox.warning(self, "Validation Error", "Please select both a room and a tenant.")
#             return

#         if self.start_date_input.date() >= self.end_date_input.date():
#             QMessageBox.warning(self, "Validation Error", "Start date must be before end date.")
#             return

#         try:
#             create_lease(room_id, tenant_id, start_date, end_date)
#             QMessageBox.information(self, "Success", "Lease created successfully!")
#             self.accept()
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Failed to create lease: {e}")



from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDateEdit, QPushButton, QDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from controllers.lease_management_controller import create_lease, fetch_available_rooms, fetch_tenants


class AddLeaseView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Lease")
        self.layout = QVBoxLayout()

        # Room Selection
        room_label = QLabel("Select Room:")
        room_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(room_label)

        self.room_selector = QComboBox()
        self.room_selector.setStyleSheet("font-size: 14px;")
        self.load_rooms()
        self.layout.addWidget(self.room_selector)

        # Tenant Selection
        tenant_label = QLabel("Select Tenant:")
        tenant_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(tenant_label)

        self.tenant_selector = QComboBox()
        self.tenant_selector.setStyleSheet("font-size: 14px;")
        self.load_tenants()
        self.layout.addWidget(self.tenant_selector)

        # Start Date
        start_date_label = QLabel("Start Date:")
        start_date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(start_date_label)

        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.start_date_input)

        # End Date
        end_date_label = QLabel("End Date:")
        end_date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(end_date_label)

        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate().addDays(30))  # Default to 30 days later
        self.end_date_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.end_date_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Lease")
        self.save_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 8px;")
        self.save_btn.clicked.connect(self.save_lease)
        button_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 8px;")
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

    def save_lease(self):
        """Save the new lease."""
        room_id = self.room_selector.currentData()
        tenant_id = self.tenant_selector.currentData()
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")

        if not room_id or not tenant_id:
            QMessageBox.warning(self, "Validation Error", "Please select both a room and a tenant.")
            return

        if self.start_date_input.date() >= self.end_date_input.date():
            QMessageBox.warning(self, "Validation Error", "Start date must be before end date.")
            return

        try:
            create_lease(room_id, tenant_id, start_date, end_date)
            QMessageBox.information(self, "Success", "Lease created successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create lease: {e}")


