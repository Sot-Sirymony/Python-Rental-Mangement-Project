
from PyQt6.QtWidgets import (
    QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QWidget, QLabel, QMessageBox, QSizePolicy
)
from functools import partial
from views.edit_rental import EditRentalView
from views.terminate_lease import TerminateLeaseView
from controllers.lease_management_controller import (
    fetch_leases, create_lease, terminate_lease
)
from controllers.rental_management_controller import fetch_room_details_with_booking,fetch_room_details_with_booking_and_payment


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
        self.room_table.setColumnCount(11)  # Removed the "Edit Lease" action
        self.room_table.setHorizontalHeaderLabels([
            "ID", "Name", "Type", "Rental Price", "Payment Frequency",
            "Security Deposit", "Grace Period", "Occupancy Status",
            "Tenant", "Booking Status", "Room Actions"
        ])
        self.layout.addWidget(self.room_table)

        # Buttons
        self.create_lease_btn = QPushButton("Create Lease")
        self.create_lease_btn.clicked.connect(self.open_create_lease_view)
        self.layout.addWidget(self.create_lease_btn)

        self.refresh_btn = QPushButton("Refresh Rooms")
        self.refresh_btn.clicked.connect(self.load_rooms)
        self.layout.addWidget(self.refresh_btn)

        self.setLayout(self.layout)
        self.load_rooms()

    def load_rooms(self):
        """Fetch and display all room details with booking information."""
        # rooms = fetch_room_details_with_booking()
        rooms = fetch_room_details_with_booking_and_payment()
        self.populate_table(rooms)

    def populate_table(self, rooms):
        """Populate the table with room data."""
        self.room_table.setRowCount(0)
        for row_data in rooms:
            row = self.room_table.rowCount()
            self.room_table.insertRow(row)

            # Populate all columns except actions
            for col, data in enumerate(row_data[:-1]):
                item = QTableWidgetItem(str(data) if data is not None else "N/A")
                self.room_table.setItem(row, col, item)

            # Add Room Actions Buttons
            self.add_room_actions(row, row_data)

    def add_room_actions(self, row, row_data):
        """Add room action buttons to the table."""
        room_actions_widget = QWidget()
        room_layout = QVBoxLayout()
        room_layout.setContentsMargins(5, 5, 5, 5)
        room_layout.setSpacing(10)

        edit_room_btn = QPushButton("Edit Room")
        edit_room_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        edit_room_btn.setMinimumHeight(30)
        edit_room_btn.clicked.connect(partial(self.open_edit_view, row_data))
        room_layout.addWidget(edit_room_btn)

        room_actions_widget.setLayout(room_layout)
        self.room_table.setCellWidget(row, 10, room_actions_widget)

    def open_create_lease_view(self):
        """Open a dialog to create a new lease."""
        from views.add_lease import CreateLeaseView
        dialog = CreateLeaseView(self)
        if dialog.exec():
            self.load_rooms()

    def open_terminate_lease_view(self, lease_data):
        """Open the terminate lease dialog for the selected lease."""
        dialog = TerminateLeaseView(lease_data, self)
        if dialog.exec():
            self.load_rooms()

    def open_edit_view(self, room_data):
        """Open the edit dialog for the selected room."""
        dialog = EditRentalView(room_data, self)
        if dialog.exec():
            self.load_rooms()

    def filter_rooms(self, status):
        """Filter rooms based on the selected status."""
        all_rooms = fetch_room_details_with_booking()
        filtered_rooms = (
            all_rooms if status == "All" else
            [room for room in all_rooms if (room[7] == status or (status == "Booked" and room[9] != "No Booking"))]
        )
        self.populate_table(filtered_rooms)


