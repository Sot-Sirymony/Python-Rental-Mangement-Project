from PyQt6.QtWidgets import (
    QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox,
    QWidget, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from controllers.PostGreSqlControllers.lease_management_controller import fetch_leases, cancel_lease, delete_lease
from views.LeaseModule.add_lease import AddLeaseView

class LeaseManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lease Management")
        self.layout = QVBoxLayout()

        # Lease Table
        self.lease_table = QTableWidget()
        self.lease_table.setColumnCount(9)  # Added "Cancel" column
        self.lease_table.setHorizontalHeaderLabels([
            "Lease ID", "Room Name", "Tenant Name", "Start Date", "End Date",
            "Status", "Edit", "Cancel", "Delete"
        ])

        # Table styling
        self.lease_table.setStyleSheet("""
            QTableWidget::item { font-size: 14px; text-align: center; }
            QHeaderView::section { font-size: 16px; font-weight: bold; text-align: center; }
        """)
        self.lease_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.layout.addWidget(self.lease_table)

        # Refresh Button
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 8px;")
        self.refresh_btn.clicked.connect(self.load_leases)
        self.layout.addWidget(self.refresh_btn)
        
        # Buttons
        self.add_lease_btn = QPushButton("Add Lease")
        self.add_lease_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 8px;")
        self.add_lease_btn.clicked.connect(self.open_add_lease_view)
        self.layout.addWidget(self.add_lease_btn)

        self.setLayout(self.layout)
        self.load_leases()

    def load_leases(self):
        """Load and display leases."""
        leases = fetch_leases()
        self.lease_table.setRowCount(0)

        for lease in leases:
            row = self.lease_table.rowCount()
            self.lease_table.insertRow(row)

            # Populate the table with lease data
            for col, data in enumerate(lease[:6]):  # Lease ID, Room Name, Tenant Name, Start/End Date, Status
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.lease_table.setItem(row, col, item)

            # Edit Button
            edit_btn = QPushButton("Edit")
            edit_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 4px;")
            edit_btn.clicked.connect(lambda _, l=lease: self.edit_lease(l))
            self.lease_table.setCellWidget(row, 6, edit_btn)

            # Cancel Button
            cancel_btn = QPushButton("Cancel")
            cancel_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 4px;")
            cancel_btn.clicked.connect(lambda _, l=lease: self.cancel_lease_action(l[0]))
            self.lease_table.setCellWidget(row, 7, cancel_btn)

            # Delete Button
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 4px;")
            delete_btn.clicked.connect(lambda _, l=lease: self.delete_lease_action(l[0]))
            self.lease_table.setCellWidget(row, 8, delete_btn)
    
    def edit_lease(self, lease):
        """Open Edit Lease dialog."""
        from views.LeaseModule.edit_lease import EditLeaseView
        dialog = EditLeaseView(lease, self)
        if dialog.exec():
            self.load_leases()

    def cancel_lease_action(self, lease_id):
        """Cancel a lease with confirmation."""
        reply = QMessageBox.question(
            self, "Cancel Lease",
            f"Are you sure you want to cancel lease ID {lease_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                cancel_lease(lease_id)
                QMessageBox.information(self, "Success", f"Lease {lease_id} canceled successfully!")
                self.load_leases()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to cancel lease: {e}")

    def delete_lease_action(self, lease_id):
        """Delete a lease."""
        reply = QMessageBox.question(
            self, "Delete Lease",
            f"Are you sure you want to delete lease ID {lease_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_lease(lease_id)
                QMessageBox.information(self, "Success", f"Lease {lease_id} deleted successfully!")
                self.load_leases()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete lease: {e}")
                
    def open_add_lease_view(self):
        """Open Add Lease dialog."""
        dialog = AddLeaseView(self)
        if dialog.exec():
            self.load_leases()            
                
