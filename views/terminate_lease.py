# from PyQt6.QtWidgets import QVBoxLayout, QDialog, QLabel, QPushButton, QTextEdit, QMessageBox
# from controllers.lease_management_controller import terminate_lease

# class TerminateLeaseView(QDialog):
#     def __init__(self, lease_data, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle(f"Terminate Lease for Room {lease_data['room_name']}")
#         self.lease_id = lease_data['id']
#         self.layout = QVBoxLayout()

#         # Lease Information
#         self.layout.addWidget(QLabel(f"Tenant: {lease_data['tenant_name']}"))
#         self.layout.addWidget(QLabel(f"Room: {lease_data['room_name']}"))
#         self.layout.addWidget(QLabel(f"End Date: {lease_data['end_date']}"))

#         # Termination Notes
#         self.layout.addWidget(QLabel("Termination Notes"))
#         self.termination_notes = QTextEdit()
#         self.layout.addWidget(self.termination_notes)

#         # Terminate Button
#         self.terminate_btn = QPushButton("Terminate Lease")
#         self.terminate_btn.clicked.connect(self.terminate_lease)
#         self.layout.addWidget(self.terminate_btn)

#         self.setLayout(self.layout)

#     def terminate_lease(self):
#         notes = self.termination_notes.toPlainText()

#         if not notes.strip():
#             QMessageBox.warning(self, "Warning", "Please provide termination notes.")
#             return

#         try:
#             terminate_lease(self.lease_id, notes)
#             QMessageBox.information(self, "Success", "Lease terminated successfully!")
#             self.accept()
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Failed to terminate lease: {e}")


from PyQt6.QtWidgets import QVBoxLayout, QDialog, QLabel, QPushButton, QMessageBox
from controllers.lease_management_controller import terminate_lease

class TerminateLeaseView(QDialog):
    def __init__(self, lease_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Terminate Lease for Room {lease_data[1]}")  # Use index 1 for room_name
        self.lease_id = lease_data[0]  # Use index 0 for lease_id
        self.layout = QVBoxLayout()

        # Lease Information (Read-Only)
        self.layout.addWidget(QLabel(f"Room: {lease_data[1]}"))  # Room name
        self.layout.addWidget(QLabel(f"Tenant: {lease_data[2]}"))  # Tenant name
        self.layout.addWidget(QLabel(f"Start Date: {lease_data[3]}"))  # Start date
        self.layout.addWidget(QLabel(f"End Date: {lease_data[4]}"))  # End date
        self.layout.addWidget(QLabel(f"Status: {lease_data[5]}"))  # Lease status

        # Terminate Button
        self.terminate_btn = QPushButton("Terminate Lease")
        self.terminate_btn.clicked.connect(self.terminate_lease)
        self.layout.addWidget(self.terminate_btn)

        # Cancel Button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_btn)

        self.setLayout(self.layout)

    def terminate_lease(self):
        """Terminate the lease."""
        try:
            terminate_lease(self.lease_id)
            QMessageBox.information(self, "Success", "Lease terminated successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to terminate lease: {e}")
            

