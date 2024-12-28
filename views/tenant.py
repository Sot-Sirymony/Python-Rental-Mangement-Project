from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QFormLayout

class TenantManagement(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Tenant Management"))

        # Add New Tenant Button
        add_tenant_btn = QPushButton("Add New Tenant")
        add_tenant_btn.clicked.connect(self.add_tenant_form)
        layout.addWidget(add_tenant_btn)

        # Tenant List Table
        self.tenant_table = QTableWidget(0, 3)  # 3 columns: Name, Phone, Email
        self.tenant_table.setHorizontalHeaderLabels(["Name", "Phone", "Email"])
        layout.addWidget(self.tenant_table)

        self.setLayout(layout)

    def add_tenant_form(self):
        form = QWidget()
        form_layout = QFormLayout()

        first_name_input = QLineEdit()
        last_name_input = QLineEdit()
        phone_input = QLineEdit()
        email_input = QLineEdit()

        form_layout.addRow("First Name", first_name_input)
        form_layout.addRow("Last Name", last_name_input)
        form_layout.addRow("Phone", phone_input)
        form_layout.addRow("Email", email_input)

        save_btn = QPushButton("Save Tenant")
        save_btn.clicked.connect(lambda: self.save_tenant(first_name_input.text(), last_name_input.text(), phone_input.text(), email_input.text()))
        form_layout.addWidget(save_btn)

        form.setLayout(form_layout)
        form.show()

    def save_tenant(self, first_name, last_name, phone, email):
        from controllers.tenant_controller import add_tenant
        add_tenant(first_name, last_name, phone, email)
        self.refresh_tenant_table()

    def refresh_tenant_table(self):
        from controllers.tenant_controller import get_all_tenants
        tenants = get_all_tenants()
        self.tenant_table.setRowCount(0)  # Clear table
        for tenant in tenants:
            row = self.tenant_table.rowCount()
            self.tenant_table.insertRow(row)
            self.tenant_table.setItem(row, 0, QTableWidgetItem(tenant['name']))
            self.tenant_table.setItem(row, 1, QTableWidgetItem(tenant['phone']))
            self.tenant_table.setItem(row, 2, QTableWidgetItem(tenant['email']))
