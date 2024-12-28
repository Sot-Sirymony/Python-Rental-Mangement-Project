
from PyQt6.QtWidgets import (
    QVBoxLayout, QLineEdit, QComboBox, QPushButton, QDialog, QLabel, QMessageBox
)
from controllers.tenant_controller import fetch_tenants
from controllers.rental_management_controller import (
    set_rental_price_and_terms, update_occupancy_status, update_tenant_for_room
)

class EditRentalView(QDialog):
    def __init__(self, room_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Rental Details")
        self.layout = QVBoxLayout()

        self.room_id = room_data[0]

        # Room Name (Display Only)
        self.layout.addWidget(QLabel(f"<b>Room Name:</b> {room_data[1]}"))

        # Rental Price
        self.layout.addWidget(QLabel("Rental Price:"))
        self.rental_price_input = QLineEdit(str(room_data[3]))
        self.rental_price_input.setPlaceholderText("Enter rental price")
        self.layout.addWidget(self.rental_price_input)

        # Payment Frequency
        self.layout.addWidget(QLabel("Payment Frequency:"))
        self.payment_frequency_input = QComboBox()
        self.payment_frequency_input.addItems(["Monthly", "Quarterly", "Yearly"])
        self.payment_frequency_input.setCurrentText(room_data[4])
        self.layout.addWidget(self.payment_frequency_input)

        # Security Deposit
        self.layout.addWidget(QLabel("Security Deposit:"))
        self.security_deposit_input = QLineEdit(str(room_data[5]))
        self.security_deposit_input.setPlaceholderText("Enter security deposit amount")
        self.layout.addWidget(self.security_deposit_input)

        # Grace Period
        self.layout.addWidget(QLabel("Grace Period (days):"))
        self.grace_period_input = QLineEdit(str(room_data[6]))
        self.grace_period_input.setPlaceholderText("Enter grace period in days")
        self.layout.addWidget(self.grace_period_input)

        # Occupancy Status
        self.layout.addWidget(QLabel("Occupancy Status:"))
        self.occupancy_status_input = QComboBox()
        self.occupancy_status_input.addItems(["Available", "Rented", "Maintenance"])
        self.occupancy_status_input.setCurrentText(room_data[7])
        self.layout.addWidget(self.occupancy_status_input)

        # Tenant Selector
        self.layout.addWidget(QLabel("Assigned Tenant:"))
        self.tenant_selector = QComboBox()
        tenants = fetch_tenants()
        self.tenant_selector.addItem("No Tenant", None)  # Allow no tenant
        for tenant in tenants:
            self.tenant_selector.addItem(f"{tenant[1]} ({tenant[2]})", tenant[0])
        if room_data[8] and room_data[8] != "No Tenant":
            for i in range(self.tenant_selector.count()):
                if self.tenant_selector.itemText(i) == room_data[8]:
                    self.tenant_selector.setCurrentIndex(i)
                    break
        self.layout.addWidget(self.tenant_selector)

        # Save Button
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

    def save_changes(self):
        try:
            # Validate Numeric Inputs
            rental_price = self.validate_numeric_input(self.rental_price_input.text(), "Rental Price")
            security_deposit = self.validate_numeric_input(self.security_deposit_input.text(), "Security Deposit")
            grace_period = self.validate_numeric_input(self.grace_period_input.text(), "Grace Period", int)

            # Retrieve Other Inputs
            payment_frequency = self.payment_frequency_input.currentText()
            occupancy_status = self.occupancy_status_input.currentText()
            tenant_id = self.tenant_selector.currentData()

            # Call Controllers
            set_rental_price_and_terms(self.room_id, rental_price, payment_frequency, security_deposit, grace_period)
            update_occupancy_status(self.room_id, occupancy_status)
            update_tenant_for_room(self.room_id, tenant_id)

            QMessageBox.information(self, "Success", "Room details updated successfully!")
            self.accept()
        except ValueError as ve:
            QMessageBox.warning(self, "Validation Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save changes: {e}")

    def validate_numeric_input(self, value, field_name, cast_type=float):
        """Validates if the input is numeric and casts it to the specified type."""
        try:
            return cast_type(value)
        except ValueError:
            raise ValueError(f"{field_name} must be a valid numeric value.")



