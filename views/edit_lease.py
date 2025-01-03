# from PyQt6.QtWidgets import (
#     QDialog, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QComboBox, QPushButton, QMessageBox
# )
# from PyQt6.QtCore import Qt, QDate
# from controllers.lease_management_controller import update_lease

# class EditLeaseView(QDialog):
#     def __init__(self, lease, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Edit Lease")
#         self.lease = lease
#         self.layout = QVBoxLayout()

#         # Lease ID
#         self.layout.addWidget(QLabel(f"Editing Lease ID: {lease[0]}"))

#         # Room Name (read-only)
#         self.layout.addWidget(QLabel("Room Name:"))
#         self.room_name_input = QLineEdit(lease[1])
#         self.room_name_input.setReadOnly(True)
#         self.layout.addWidget(self.room_name_input)

#         # Tenant Name (read-only)
#         self.layout.addWidget(QLabel("Tenant Name:"))
#         self.tenant_name_input = QLineEdit(lease[2])
#         self.tenant_name_input.setReadOnly(True)
#         self.layout.addWidget(self.tenant_name_input)

#         # Start Date
#         self.layout.addWidget(QLabel("Start Date:"))
#         self.start_date_input = QDateEdit(QDate.fromString(lease[3], "yyyy-MM-dd"))
#         self.start_date_input.setCalendarPopup(True)
#         self.layout.addWidget(self.start_date_input)

#         # End Date
#         self.layout.addWidget(QLabel("End Date:"))
#         self.end_date_input = QDateEdit(QDate.fromString(lease[4], "yyyy-MM-dd"))
#         self.end_date_input.setCalendarPopup(True)
#         self.layout.addWidget(self.end_date_input)

#         # Status
#         self.layout.addWidget(QLabel("Status:"))
#         self.status_input = QComboBox()
#         self.status_input.addItems(["Active", "Completed", "Canceled","Active"])
#         self.status_input.setCurrentText(lease[5])
#         self.layout.addWidget(self.status_input)

#         # Save Button
#         self.save_btn = QPushButton("Save Changes")
#         self.save_btn.clicked.connect(self.save_changes)
#         self.layout.addWidget(self.save_btn)

#         self.setLayout(self.layout)

#     def save_changes(self):
#         """Save changes to the lease."""
#         start_date = self.start_date_input.date().toString("yyyy-MM-dd")
#         end_date = self.end_date_input.date().toString("yyyy-MM-dd")
#         status = self.status_input.currentText()

#         # Validate dates
#         if QDate.fromString(start_date, "yyyy-MM-dd") > QDate.fromString(end_date, "yyyy-MM-dd"):
#             QMessageBox.critical(self, "Error", "Start date cannot be after end date.")
#             return

#         # Automatic Updates
#         if QDate.currentDate() > QDate.fromString(end_date, "yyyy-MM-dd"):
#             status = "Completed"

#         try:
#             update_lease(self.lease[0], start_date, end_date, status)
#             QMessageBox.information(self, "Success", "Lease updated successfully!")
#             self.accept()  # Close dialog
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Failed to update lease: {e}")






from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QComboBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from controllers.lease_management_controller import update_lease

class EditLeaseView(QDialog):
    def __init__(self, lease, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Lease")
        self.lease = lease
        self.layout = QVBoxLayout()

        # Lease ID
        lease_id_label = QLabel(f"Editing Lease ID: {lease[0]}")
        lease_id_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(lease_id_label)

        # Room Name (read-only)
        room_name_label = QLabel("Room Name:")
        room_name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(room_name_label)

        self.room_name_input = QLineEdit(lease[1])
        self.room_name_input.setReadOnly(True)
        self.room_name_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.room_name_input)

        # Tenant Name (read-only)
        tenant_name_label = QLabel("Tenant Name:")
        tenant_name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(tenant_name_label)

        self.tenant_name_input = QLineEdit(lease[2])
        self.tenant_name_input.setReadOnly(True)
        self.tenant_name_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.tenant_name_input)

        # Start Date
        start_date_label = QLabel("Start Date:")
        start_date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(start_date_label)

        self.start_date_input = QDateEdit(QDate.fromString(lease[3], "yyyy-MM-dd"))
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.start_date_input)

        # End Date
        end_date_label = QLabel("End Date:")
        end_date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(end_date_label)

        self.end_date_input = QDateEdit(QDate.fromString(lease[4], "yyyy-MM-dd"))
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.end_date_input)

        # Status
        status_label = QLabel("Status:")
        status_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(status_label)

        self.status_input = QComboBox()
        self.status_input.addItems(["Active", "Completed", "Canceled"])
        self.status_input.setCurrentText(lease[5])
        self.status_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.status_input)

        # Save Button
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 8px;")
        self.save_btn.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

    def save_changes(self):
        """Save changes to the lease."""
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")
        status = self.status_input.currentText()

        # Validate dates
        if QDate.fromString(start_date, "yyyy-MM-dd") > QDate.fromString(end_date, "yyyy-MM-dd"):
            QMessageBox.critical(self, "Error", "Start date cannot be after end date.")
            return

        # Automatic Updates
        if QDate.currentDate() > QDate.fromString(end_date, "yyyy-MM-dd"):
            status = "Completed"

        try:
            update_lease(self.lease[0], start_date, end_date, status)
            QMessageBox.information(self, "Success", "Lease updated successfully!")
            self.accept()  # Close dialog
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update lease: {e}")

