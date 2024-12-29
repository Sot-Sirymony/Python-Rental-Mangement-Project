


# from PyQt6.QtWidgets import (
#     QDialog, QVBoxLayout, QLabel, QComboBox, QDateEdit, QTextEdit, QPushButton, QMessageBox
# )
# from controllers.booking_controller import update_booking
# from controllers.property_controller import fetch_available_rooms
# from controllers.tenant_controller import fetch_tenants
# from PyQt6.QtCore import QDate

# class EditBookingView(QDialog):  # Use QDialog for modal behavior
#     def __init__(self, booking_data, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Edit Booking")
#         self.setModal(True)  # Ensure modal behavior
#         self.resize(400, 450)
#         print("Booking Data in Edit View:", booking_data)

#         self.booking_id = booking_data[0]

#         self.layout = QVBoxLayout()

#         # Room Selector
#         self.layout.addWidget(QLabel("Select Room"))
#         self.room_selector = QComboBox()
#         rooms = fetch_available_rooms()
#         for room in rooms:
#             self.room_selector.addItem(f"{room[1]} ({room[0]})", room[0])
#         self.room_selector.setCurrentText(booking_data[1])
#         self.layout.addWidget(self.room_selector)

#         # Tenant Selector
#         self.layout.addWidget(QLabel("Select Tenant"))
#         self.tenant_selector = QComboBox()
#         tenants = fetch_tenants()
#         for tenant in tenants:
#             self.tenant_selector.addItem(f"{tenant[1]} {tenant[2]}", tenant[0])
#         self.tenant_selector.setCurrentText(booking_data[2])
#         self.layout.addWidget(self.tenant_selector)

#         # Booking Dates
#         self.layout.addWidget(QLabel("Start Date"))
#         self.start_date = QDateEdit()
#         self.start_date.setCalendarPopup(True)
#         self.start_date.setDisplayFormat("yyyy-MM-dd")
#         self.start_date.setDate(QDate.fromString(booking_data[3], "yyyy-MM-dd"))
#         self.layout.addWidget(self.start_date)

#         self.layout.addWidget(QLabel("End Date"))
#         self.end_date = QDateEdit()
#         self.end_date.setCalendarPopup(True)
#         self.end_date.setDisplayFormat("yyyy-MM-dd")
#         self.end_date.setDate(QDate.fromString(booking_data[4], "yyyy-MM-dd"))
#         self.layout.addWidget(self.end_date)

#         # Booking Status
#         self.layout.addWidget(QLabel("Select Status"))
#         self.status_selector = QComboBox()
#         self.status_selector.addItems(["Pending", "Active", "Canceled", "Completed"])
#         self.status_selector.setCurrentText(booking_data[5])
#         self.layout.addWidget(self.status_selector)

#         # Booking Notes
#         self.layout.addWidget(QLabel("Notes"))
#         self.notes_input = QTextEdit()
#         self.notes_input.setPlainText(booking_data[6])  # Pre-fill notes
#         self.layout.addWidget(self.notes_input)

#         # Save Button
#         self.save_btn = QPushButton("Save Changes")
#         self.save_btn.clicked.connect(self.save_booking)
#         self.layout.addWidget(self.save_btn)

#         self.setLayout(self.layout)

#     def save_booking(self):
#         # Collect updated booking data
#         room_id = self.room_selector.currentData()
#         tenant_id = self.tenant_selector.currentData()
#         start_date = self.start_date.date().toString("yyyy-MM-dd")
#         end_date = self.end_date.date().toString("yyyy-MM-dd")
#         status = self.status_selector.currentText()
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
#             update_booking(self.booking_id, room_id, tenant_id, start_date, end_date, notes, status)
#             QMessageBox.information(self, "Success", "Booking updated successfully!")
#             if self.parent():
#                 self.parent().load_bookings()  # Refresh the parent view
#             self.accept()
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Failed to update booking: {e}")



from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QDateEdit, QTextEdit, QPushButton, QMessageBox
)
from controllers.booking_controller import update_booking
from controllers.property_controller import fetch_available_rooms
from controllers.tenant_controller import fetch_tenants
from PyQt6.QtCore import QDate
import sqlite3
from controllers.booking_controller import (
    update_booking,
    set_room_status_rented,
    set_room_status_available_if_no_active_or_pending,
    set_room_status_available,
)

class EditBookingView(QDialog):  # Use QDialog for modal behavior
    # def __init__(self, booking_data, parent=None):
    #     super().__init__(parent)
    #     self.setWindowTitle("Edit Booking")
    #     self.setModal(True)  # Ensure modal behavior
    #     self.resize(400, 450)
    #     print("Booking Data in Edit View:", booking_data)

    #     self.booking_id = booking_data[0]

    #     self.layout = QVBoxLayout()

    #     # Room Selector
    #     self.layout.addWidget(QLabel("Select Room"))
    #     self.room_selector = QComboBox()
    #     rooms = fetch_available_rooms()
    #     for room in rooms:
    #         self.room_selector.addItem(f"{room[1]} ({room[0]})", room[0])
    #     self.room_selector.setCurrentText(booking_data[1])
    #     self.layout.addWidget(self.room_selector)

    #     # Tenant Selector
    #     self.layout.addWidget(QLabel("Select Tenant"))
    #     self.tenant_selector = QComboBox()
    #     tenants = fetch_tenants()
    #     for tenant in tenants:
    #         self.tenant_selector.addItem(f"{tenant[1]} {tenant[2]}", tenant[0])
    #     self.tenant_selector.setCurrentText(booking_data[2])
    #     self.layout.addWidget(self.tenant_selector)

    #     # Booking Dates
    #     self.layout.addWidget(QLabel("Start Date"))
    #     self.start_date = QDateEdit()
    #     self.start_date.setCalendarPopup(True)
    #     self.start_date.setDisplayFormat("yyyy-MM-dd")
    #     self.start_date.setDate(QDate.fromString(booking_data[3], "yyyy-MM-dd"))
    #     self.layout.addWidget(self.start_date)

    #     self.layout.addWidget(QLabel("End Date"))
    #     self.end_date = QDateEdit()
    #     self.end_date.setCalendarPopup(True)
    #     self.end_date.setDisplayFormat("yyyy-MM-dd")
    #     self.end_date.setDate(QDate.fromString(booking_data[4], "yyyy-MM-dd"))
    #     self.layout.addWidget(self.end_date)

    #     # Booking Status
    #     self.layout.addWidget(QLabel("Select Status"))
    #     self.status_selector = QComboBox()
    #     self.status_selector.addItems(["Pending", "Active", "Canceled", "Completed"])
    #     self.status_selector.setCurrentText(booking_data[5])
    #     self.layout.addWidget(self.status_selector)

    #     # Booking Notes
    #     self.layout.addWidget(QLabel("Notes"))
    #     self.notes_input = QTextEdit()
    #     self.notes_input.setPlainText(booking_data[6])  # Pre-fill notes
    #     self.layout.addWidget(self.notes_input)

    #     # Save Button
    #     self.save_btn = QPushButton("Save Changes")
    #     self.save_btn.clicked.connect(self.save_booking)
    #     self.layout.addWidget(self.save_btn)

    #     self.setLayout(self.layout)
    
    def __init__(self, booking_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Booking")
        self.setModal(True)  # Ensure modal behavior
        self.resize(400, 450)
       #print("Booking Data in Edit View:", booking_data)

        self.booking_id = booking_data[0]

        self.layout = QVBoxLayout()

        # Room Selector
        self.layout.addWidget(QLabel("Select Room"))
        self.room_selector = QComboBox()
        rooms = fetch_available_rooms()
        print("Booking Data in Edit View:", booking_data)
        for room in rooms:
            self.room_selector.addItem(f"{room[1]} ({room[0]})", room[0])
        self.room_selector.setCurrentText(booking_data[1])
        self.layout.addWidget(self.room_selector)

        # Tenant Selector
        self.layout.addWidget(QLabel("Select Tenant"))
        self.tenant_selector = QComboBox()
        tenants = fetch_tenants()
        for tenant in tenants:
            self.tenant_selector.addItem(f"{tenant[1]} {tenant[2]}", tenant[0])
        self.tenant_selector.setCurrentText(booking_data[2])
        self.layout.addWidget(self.tenant_selector)

        # Booking Dates
        self.layout.addWidget(QLabel("Start Date"))
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        self.start_date.setDate(QDate.fromString(booking_data[3], "yyyy-MM-dd"))
        self.layout.addWidget(self.start_date)

        self.layout.addWidget(QLabel("End Date"))
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDisplayFormat("yyyy-MM-dd")
        self.end_date.setDate(QDate.fromString(booking_data[4], "yyyy-MM-dd"))
        self.layout.addWidget(self.end_date)

        # Booking Status
        self.layout.addWidget(QLabel("Select Status"))
        self.status_selector = QComboBox()
        self.status_selector.addItems(["Pending", "Active", "Canceled", "Completed"])
        self.status_selector.setCurrentText(booking_data[5])
        self.layout.addWidget(self.status_selector)

        # Booking Notes
        self.layout.addWidget(QLabel("Notes"))
        self.notes_input = QTextEdit()
        self.notes_input.setPlainText(booking_data[6])  # Pre-fill notes
        self.layout.addWidget(self.notes_input)

        # Save Button
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.save_booking)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

    # def save_booking(self):
    #     # Collect updated booking data
    #     room_id = self.room_selector.currentData()
    #     tenant_id = self.tenant_selector.currentData()
    #     start_date = self.start_date.date().toString("yyyy-MM-dd")
    #     end_date = self.end_date.date().toString("yyyy-MM-dd")
    #     status = self.status_selector.currentText()
    #     notes = self.notes_input.toPlainText()

    #     # Validation
    #     if not room_id:
    #         QMessageBox.warning(self, "Validation Error", "Please select a room.")
    #         return
    #     if not tenant_id:
    #         QMessageBox.warning(self, "Validation Error", "Please select a tenant.")
    #         return
    #     if self.start_date.date() > self.end_date.date():
    #         QMessageBox.warning(self, "Validation Error", "Start date must be before the end date.")
    #         return

    #     try:
    #         # Update the booking
    #         update_booking(self.booking_id, room_id, tenant_id, start_date, end_date, notes, status)

    #         # Update room occupancy status based on booking status
    #         connection = sqlite3.connect('rental_management_v2.db')
    #         cursor = connection.cursor()
    #         if status == "Active":
    #             cursor.execute("UPDATE Room SET occupancy_status = 'Rented' WHERE id = ?", (room_id,))
    #         elif status == "Canceled":
    #             cursor.execute("""
    #                 UPDATE Room
    #                 SET occupancy_status = 'Available'
    #                 WHERE id = ?
    #                 AND NOT EXISTS (
    #                     SELECT 1 FROM Booking
    #                     WHERE room_id = ? AND status IN ('Active', 'Pending')
    #                 )
    #             """, (room_id, room_id))
    #         elif status == "Pending":
    #             cursor.execute("UPDATE Room SET occupancy_status = 'Available' WHERE id = ?", (room_id,))
    #         connection.commit()
    #         connection.close()

    #         QMessageBox.information(self, "Success", "Booking and room status updated successfully!")
    #         if self.parent():
    #             self.parent().load_bookings()  # Refresh the parent view
    #         self.accept()
    #     except Exception as e:
    #         QMessageBox.critical(self, "Error", f"Failed to update booking: {e}")
    
    def save_booking(self):
        # Collect updated booking data
        room_id = self.room_selector.currentData()
        tenant_id = self.tenant_selector.currentData()
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        status = self.status_selector.currentText()
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
            # Update the booking
            update_booking(self.booking_id, room_id, tenant_id, start_date, end_date, notes, status)

            # Update room occupancy status based on booking status
            if status == "Active":
                set_room_status_rented(room_id)
            elif status == "Canceled":
                set_room_status_available_if_no_active_or_pending(room_id)
            elif status == "Pending":
                set_room_status_available(room_id)

            QMessageBox.information(self, "Success", "Booking and room status updated successfully!")
            if self.parent():
                self.parent().load_bookings()  # Refresh the parent view
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update booking: {e}")
