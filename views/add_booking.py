


# from PyQt6.QtWidgets import (
#     QDialog, QVBoxLayout, QLabel, QComboBox, QDateEdit, QTextEdit, QPushButton, QMessageBox
# )
# from controllers.booking_controller import add_booking
# from controllers.property_controller import fetch_available_rooms
# from controllers.tenant_controller import fetch_tenants

# class AddBookingView(QDialog):  # Use QDialog instead of QWidget
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Add Booking")
#         self.setModal(True)  # Make the dialog modal
#         self.resize(400, 400)  # Set an appropriate size for the dialog

#         self.layout = QVBoxLayout()

#         # Room Selector
#         self.layout.addWidget(QLabel("Select Room"))
#         self.room_selector = QComboBox()
#         try:
#             rooms = fetch_available_rooms()
#             if not rooms:
#                 self.room_selector.addItem("No available rooms", None)
#             else:
#                 for room in rooms:
#                     self.room_selector.addItem(f"{room[1]} ({room[0]})", room[0])  # Display name, store ID
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Failed to fetch rooms: {e}")
#         self.layout.addWidget(self.room_selector)

#         # Tenant Selector
#         self.layout.addWidget(QLabel("Select Tenant"))
#         self.tenant_selector = QComboBox()
#         try:
#             tenants = fetch_tenants()
#             if not tenants:
#                 self.tenant_selector.addItem("No tenants found", None)
#             else:
#                 for tenant in tenants:
#                     self.tenant_selector.addItem(f"{tenant[1]} {tenant[2]}", tenant[0])  # Display name, store ID
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Failed to fetch tenants: {e}")
#         self.layout.addWidget(self.tenant_selector)

#         # Booking Dates
#         self.layout.addWidget(QLabel("Start Date"))
#         self.start_date = QDateEdit()
#         self.start_date.setCalendarPopup(True)
#         self.start_date.setDisplayFormat("yyyy-MM-dd")
#         self.layout.addWidget(self.start_date)

#         self.layout.addWidget(QLabel("End Date"))
#         self.end_date = QDateEdit()
#         self.end_date.setCalendarPopup(True)
#         self.end_date.setDisplayFormat("yyyy-MM-dd")
#         self.layout.addWidget(self.end_date)

#         # Booking Notes
#         self.layout.addWidget(QLabel("Notes"))
#         self.notes_input = QTextEdit()
#         self.layout.addWidget(self.notes_input)

#         # Save Button
#         self.save_btn = QPushButton("Save Booking")
#         self.save_btn.clicked.connect(self.save_booking)
#         self.layout.addWidget(self.save_btn)

#         # Layout Settings
#         self.layout.setSpacing(10)
#         self.layout.setContentsMargins(20, 20, 20, 20)
#         self.setLayout(self.layout)

#     def save_booking(self):
#         room_id = self.room_selector.currentData()
#         tenant_id = self.tenant_selector.currentData()
#         start_date = self.start_date.date().toString("yyyy-MM-dd")
#         end_date = self.end_date.date().toString("yyyy-MM-dd")
#         notes = self.notes_input.toPlainText()

#         # Validation
#         if not room_id:
#             QMessageBox.warning(self, "Validation Error", "Please select a room.")
#             return
#         if not tenant_id:
#             QMessageBox.warning(self, "Validation Error", "Please select a tenant.")
#             return
#         if self.start_date.date() > self.end_date.date():
#             QMessageBox.warning(self, "Validation Error", "Start date must be before the end date.")
#             return

#         try:
#             add_booking(room_id, tenant_id, start_date, end_date, notes)
#             QMessageBox.information(self, "Success", "Booking added successfully!")
#             if self.parent():
#                 self.parent().load_bookings()  # Refresh parent view
#             self.accept()  # Close the dialog
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Failed to add booking: {e}")





from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QDateEdit, QTextEdit, QPushButton, QMessageBox
)
from controllers.booking_controller import add_booking
from controllers.property_controller import fetch_available_rooms
from controllers.tenant_controller import fetch_tenants


class AddBookingView(QDialog):  # Use QDialog for modal behavior
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Booking")
        self.setModal(True)  # Make the dialog modal
        self.resize(400, 450)  # Set an appropriate size for the dialog

        self.layout = QVBoxLayout()

        # Room Selector
        self.layout.addWidget(QLabel("Select Room"))
        self.room_selector = QComboBox()
        try:
            rooms = fetch_available_rooms()
            if not rooms:
                self.room_selector.addItem("No available rooms", None)
            else:
                for room in rooms:
                    self.room_selector.addItem(f"{room[1]} ({room[0]})", room[0])  # Display name, store ID
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch rooms: {e}")
        self.layout.addWidget(self.room_selector)

        # Tenant Selector
        self.layout.addWidget(QLabel("Select Tenant"))
        self.tenant_selector = QComboBox()
        try:
            tenants = fetch_tenants()
            if not tenants:
                self.tenant_selector.addItem("No tenants found", None)
            else:
                for tenant in tenants:
                    self.tenant_selector.addItem(f"{tenant[1]} {tenant[2]}", tenant[0])  # Display name, store ID
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch tenants: {e}")
        self.layout.addWidget(self.tenant_selector)

        # Booking Dates
        self.layout.addWidget(QLabel("Start Date"))
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        self.layout.addWidget(self.start_date)

        self.layout.addWidget(QLabel("End Date"))
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDisplayFormat("yyyy-MM-dd")
        self.layout.addWidget(self.end_date)

        # Booking Status Selector
        self.layout.addWidget(QLabel("Select Status"))
        self.status_selector = QComboBox()
        self.status_selector.addItems(["Pending", "Active", "Canceled", "Completed"])  # Status options
        self.layout.addWidget(self.status_selector)

        # Booking Notes
        self.layout.addWidget(QLabel("Notes"))
        self.notes_input = QTextEdit()
        self.layout.addWidget(self.notes_input)

        # Save Button
        self.save_btn = QPushButton("Save Booking")
        self.save_btn.clicked.connect(self.save_booking)
        self.layout.addWidget(self.save_btn)

        # Layout Settings
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

    def save_booking(self):
        room_id = self.room_selector.currentData()
        tenant_id = self.tenant_selector.currentData()
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        status = self.status_selector.currentText()  # Get selected status
        notes = self.notes_input.toPlainText()

        # Validation
        if not room_id:
            QMessageBox.warning(self, "Validation Error", "Please select a room.")
            return
        if not tenant_id:
            QMessageBox.warning(self, "Validation Error", "Please select a tenant.")
            return
        if self.start_date.date() > self.end_date.date():
            QMessageBox.warning(self, "Validation Error", "Start date must be before the end date.")
            return

        try:
            add_booking(room_id, tenant_id, start_date, end_date, notes, status)
            QMessageBox.information(self, "Success", "Booking added successfully!")
            if self.parent():
                self.parent().load_bookings()  # Refresh parent view
            self.accept()  # Close the dialog
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add booking: {e}")
