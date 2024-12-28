from PyQt6.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel, QComboBox, QWidget

class TenantManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tenant Management")
        self.layout = QVBoxLayout()

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Tenant by Name or Contact")
        self.search_input.textChanged.connect(self.search_tenants)
        self.layout.addWidget(self.search_input)

        # Tenant Table
        self.tenant_table = QTableWidget()
        self.tenant_table.setColumnCount(5)  # ID, Name, Contact, Actions (Edit, Delete)
        self.tenant_table.setHorizontalHeaderLabels(["ID", "Name", "Contact", "Rental History", "Actions"])
        self.layout.addWidget(self.tenant_table)

        # Buttons
        self.add_tenant_btn = QPushButton("Add Tenant")
        self.add_tenant_btn.clicked.connect(self.open_add_tenant_view)
        self.layout.addWidget(self.add_tenant_btn)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load_tenants)
        self.layout.addWidget(self.refresh_btn)

        self.setLayout(self.layout)
        self.load_tenants()

    def load_tenants(self):
        from controllers.tenant_controller import fetch_tenants
        tenants = fetch_tenants()
        self.tenant_table.setRowCount(0)
        for tenant in tenants:
            row = self.tenant_table.rowCount()
            self.tenant_table.insertRow(row)
            for col, data in enumerate(tenant[:3]):  # ID, Name, Contact
                self.tenant_table.setItem(row, col, QTableWidgetItem(str(data)))

            # Add View Rental History Button
            history_btn = QPushButton("View History")
            history_btn.clicked.connect(lambda _, t=tenant: self.view_rental_history(t))
            self.tenant_table.setCellWidget(row, 3, history_btn)

            # Add Edit Button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, t=tenant: self.open_edit_tenant_view(t))
            self.tenant_table.setCellWidget(row, 4, edit_btn)

    def search_tenants(self, search_text):
        from controllers.tenant_controller import fetch_tenants
        tenants = fetch_tenants()
        filtered_tenants = [tenant for tenant in tenants if search_text.lower() in tenant[1].lower() or search_text.lower() in tenant[2].lower()]
        self.tenant_table.setRowCount(0)
        for tenant in filtered_tenants:
            row = self.tenant_table.rowCount()
            self.tenant_table.insertRow(row)
            for col, data in enumerate(tenant[:3]):  # ID, Name, Contact
                self.tenant_table.setItem(row, col, QTableWidgetItem(str(data)))

            # Add View Rental History Button
            history_btn = QPushButton("View History")
            history_btn.clicked.connect(lambda _, t=tenant: self.view_rental_history(t))
            self.tenant_table.setCellWidget(row, 3, history_btn)

            # Add Edit Button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, t=tenant: self.open_edit_tenant_view(t))
            self.tenant_table.setCellWidget(row, 4, edit_btn)

    def open_add_tenant_view(self):
        from views.add_tenant import AddTenantView
        dialog = AddTenantView(self)
        if dialog.exec():
            self.load_tenants()

    def open_edit_tenant_view(self, tenant_data):
        from views.edit_tenant import EditTenantView
        dialog = EditTenantView(tenant_data, self)
        if dialog.exec():
            self.load_tenants()

    def view_rental_history(self, tenant_data):
        from views.rental_history import RentalHistoryView
        dialog = RentalHistoryView(tenant_data, self)
        dialog.exec()
