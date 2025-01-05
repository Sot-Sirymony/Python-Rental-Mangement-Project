
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QComboBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from controllers.PostGreSqlControllers.lease_management_controller import update_lease

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
        self._add_label_input_pair("Room Name:", lease[1], read_only=True)

        # Tenant Name (read-only)
        self._add_label_input_pair("Tenant Name:", lease[2], read_only=True)

        # Start Date
        start_date_label = QLabel("Start Date:")
        start_date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(start_date_label)
        self.start_date_input = QDateEdit(QDate.fromString(lease[3].strftime("%Y-%m-%d"), "yyyy-MM-dd"))
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.start_date_input)

        # End Date
        end_date_label = QLabel("End Date:")
        end_date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(end_date_label)
        self.end_date_input = QDateEdit(QDate.fromString(lease[4].strftime("%Y-%m-%d"), "yyyy-MM-dd"))
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.end_date_input)

        # Status
        self._add_combo_box("Status:", ["Active", "Completed", "Canceled"], lease[5])

        # Save Button
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 8px;")
        self.save_btn.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

    def _add_label_input_pair(self, label_text, input_text, read_only=False):
        """Helper method to add label and input pair."""
        label = QLabel(label_text)
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(label)

        input_field = QLineEdit(input_text)
        input_field.setReadOnly(read_only)
        input_field.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(input_field)

    def _add_combo_box(self, label_text, items, current_text):
        """Helper method to add label and combo box."""
        label = QLabel(label_text)
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(label)

        combo_box = QComboBox()
        combo_box.addItems(items)
        combo_box.setCurrentText(current_text)
        combo_box.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(combo_box)
        self.status_input = combo_box

    def save_changes(self):
        """Save changes to the lease."""
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")
        status = self.status_input.currentText()

        # Debugging inputs
        print(f"Debug: start_date={start_date}, end_date={end_date}, status={status}")

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
