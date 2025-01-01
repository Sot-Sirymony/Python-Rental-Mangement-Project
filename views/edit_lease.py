
from PyQt6.QtWidgets import QVBoxLayout, QDialog, QLabel, QDateEdit, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtCore import QDate
from controllers.lease_management_controller import update_lease

class EditLeaseView(QDialog):
    def __init__(self, lease_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit Lease for Room {lease_data[1]}")
        self.lease_id = lease_data[0]
        self.layout = QVBoxLayout()

        # Tenant Information (Read-Only)
        self.layout.addWidget(QLabel(f"Tenant: {lease_data[2]}"))

        # Room Information (Read-Only)
        self.layout.addWidget(QLabel(f"Room: {lease_data[1]}"))

        # Start Date (Read-Only)
        self.layout.addWidget(QLabel("Start Date"))
        start_date_str = self.format_date(lease_data[3])  # Format the start date
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(start_date_str)
        self.start_date.setEnabled(False)  # Read-only
        self.layout.addWidget(self.start_date)

        # End Date (Editable)
        self.layout.addWidget(QLabel("End Date"))
        end_date_str = self.format_date(lease_data[4])  # Format the end date
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(end_date_str)
        self.layout.addWidget(self.end_date)

        # Payment Terms (Editable)
        self.layout.addWidget(QLabel("Payment Terms"))
        self.payment_terms = QLineEdit()
        self.payment_terms.setText(lease_data[5] if len(lease_data) > 5 else "")
        self.layout.addWidget(self.payment_terms)

        # Save Button
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.update_lease)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

    def update_lease(self):
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        payment_terms = self.payment_terms.text()

        try:
            update_lease(self.lease_id, self.start_date.date().toString("yyyy-MM-dd"), end_date, payment_terms)
            QMessageBox.information(self, "Success", "Lease updated successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update lease: {e}")
