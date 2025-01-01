
from PyQt6.QtWidgets import (
    QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QWidget, QLabel, QMessageBox, QSizePolicy, QHBoxLayout
)
from functools import partial
from views.edit_rental import EditRentalView
from controllers.rental_management_controller import fetch_room_details_with_related_data

class RentalManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rental Management")
        self.layout = QVBoxLayout()

        # Filter Dropdown
        self.filter_input = QComboBox()
        self.filter_input.addItems(["All", "Available", "Rented", "Maintenance", "Booked"])
        self.filter_input.currentTextChanged.connect(self.filter_rooms)
        self.layout.addWidget(self.filter_input)

        # Room Table
        self.room_table = QTableWidget()
        self.room_table.setColumnCount(16)  # Updated to include lease details
        self.room_table.setHorizontalHeaderLabels([
            "Room ID", "Room Name", "Room Type", "Rental Price", "Payment Frequency",
            "Security Deposit", "Grace Period", "Occupancy Status", "Tenant Name",
            "Dynamic Status", "Total Payments", "Last Payment Date", "Latest Due Date",
            "Payment References", "Lease Start Date", "Lease End Date"
        ])
        self.layout.addWidget(self.room_table)

        # Buttons
        button_layout = QHBoxLayout()

        self.refresh_btn = QPushButton("Refresh Rooms")
        self.refresh_btn.clicked.connect(self.load_rooms)
        button_layout.addWidget(self.refresh_btn)

        self.create_lease_btn = QPushButton("Create Lease")
        self.create_lease_btn.clicked.connect(self.open_create_lease_view)
        button_layout.addWidget(self.create_lease_btn)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        self.load_rooms()

    def load_rooms(self):
        """Fetch and display all room details with related data."""
        try:
            rooms = fetch_room_details_with_related_data()
            self.populate_table(rooms)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load room data: {e}")

    def populate_table(self, rooms):
        """Populate the table with room data."""
        self.room_table.setRowCount(0)
        for row_data in rooms:
            row = self.room_table.rowCount()
            self.room_table.insertRow(row)

            # Populate all columns with room data
            for col, data in enumerate(row_data):
                item = QTableWidgetItem(str(data) if data is not None else "N/A")
                self.room_table.setItem(row, col, item)

            # Add action buttons
            self.add_room_actions(row, row_data)

    def add_room_actions(self, row, row_data):
        """Add action buttons to the table."""
        action_widget = QWidget()
        action_layout = QHBoxLayout()
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setSpacing(5)

        edit_btn = QPushButton("Edit Room")
        edit_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        edit_btn.clicked.connect(partial(self.open_edit_view, row_data))
        action_layout.addWidget(edit_btn)

        view_lease_btn = QPushButton("View Lease")
        view_lease_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        view_lease_btn.clicked.connect(partial(self.view_lease_details, row_data))
        action_layout.addWidget(view_lease_btn)

        action_widget.setLayout(action_layout)
        self.room_table.setCellWidget(row, 15, action_widget)  # Assuming the last column index is 15

    def filter_rooms(self, status):
        """Filter rooms based on the selected status."""
        try:
            all_rooms = fetch_room_details_with_related_data()
            filtered_rooms = (
                all_rooms if status == "All" else
                [room for room in all_rooms if (room[7] == status or (status == "Booked" and room[9] != "No Booking"))]
            )
            self.populate_table(filtered_rooms)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to filter room data: {e}")

    def open_edit_view(self, room_data):
        """Open the edit dialog for the selected room."""
        dialog = EditRentalView(room_data, self)
        if dialog.exec():
            self.load_rooms()

    def open_create_lease_view(self):
        """Open a dialog to create a new lease."""
        from views.add_lease import CreateLeaseView
        dialog = CreateLeaseView(self)
        if dialog.exec():
            self.load_rooms()

    def view_lease_details(self, room_data):
        """View lease details for a selected room."""
        from views.lease_details import LeaseDetailsView
        dialog = LeaseDetailsView(room_data, self)
        dialog.exec()
