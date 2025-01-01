from PyQt6.QtWidgets import QVBoxLayout,QMessageBox, QTableWidget, QTableWidgetItem, QDialog

class RentalHistoryView(QDialog):
    def __init__(self, tenant_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Rental History for {tenant_data[1]}")
        self.layout = QVBoxLayout()

        # Rental History Table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "Room", "Start Date", "End Date", "Amount", "Payment Date", "Payment Method"
        ])
        self.layout.addWidget(self.history_table)

        self.setLayout(self.layout)
        self.load_rental_history(tenant_data[0])

    # def load_rental_history(self, tenant_id):
    #     from controllers.tenant_controller import fetch_rental_history
    #     history = fetch_rental_history(tenant_id)
    #     self.history_table.setRowCount(0)
    #     for row_data in history:
    #         row = self.history_table.rowCount()
    #         self.history_table.insertRow(row)
    #         for col, data in enumerate(row_data):
    #             self.history_table.setItem(row, col, QTableWidgetItem(str(data)))
    
    def load_rental_history(self, tenant_id):
        from controllers.tenant_controller import fetch_rental_history
        try:
            history = fetch_rental_history(tenant_id)
            print(f"Fetched rental history for tenant {tenant_id}: {history}")  # Debug: Print fetched history
            if not history:
                QMessageBox.information(self, "No Data", "No rental history found for this tenant.")
                return

            self.history_table.setRowCount(0)
            for row_data in history:
                row = self.history_table.rowCount()
                self.history_table.insertRow(row)
                for col, data in enumerate(row_data):
                    self.history_table.setItem(row, col, QTableWidgetItem(str(data) if data is not None else "N/A"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load rental history: {e}")

