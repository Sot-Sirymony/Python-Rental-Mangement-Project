

from PyQt6.QtWidgets import QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QLabel
from views.edit_rental import EditRentalView  # Import the EditRentalView dialog
from controllers.rental_management_controller import fetch_room_details


# class RentalManagement(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Rental Management")
#         self.layout = QVBoxLayout()

#         # Filter Dropdown
#         self.filter_input = QComboBox()
#         self.filter_input.addItems(["All", "Available", "Rented", "Maintenance"])
#         self.filter_input.currentTextChanged.connect(self.filter_rooms)
#         self.layout.addWidget(self.filter_input)

#         # Room Table
#         self.room_table = QTableWidget()
#         self.room_table.setColumnCount(10)  # Adding an "Actions" column
#         self.room_table.setHorizontalHeaderLabels([
#             "ID", "Name", "Type", "Rental Price", "Payment Frequency", 
#             "Security Deposit", "Grace Period", "Occupancy Status", 
#             "Tenant", "Actions"
#         ])
#         self.layout.addWidget(self.room_table)

#         # Buttons
#         self.refresh_btn = QPushButton("Refresh Rooms")
#         self.refresh_btn.clicked.connect(self.load_rooms)
#         self.layout.addWidget(self.refresh_btn)

#         self.setLayout(self.layout)
#         self.load_rooms()

#     def load_rooms(self):
#         rooms = fetch_room_details()  # Fetch rooms with tenant data
#         self.room_table.setRowCount(0)
#         for row_data in rooms:
#             row = self.room_table.rowCount()
#             self.room_table.insertRow(row)
#             for col, data in enumerate(row_data):  # Populate all columns except actions
#                 self.room_table.setItem(row, col, QTableWidgetItem(str(data)))

#             # Add Edit Button
#             edit_btn = QPushButton("Edit")
#             edit_btn.clicked.connect(lambda _, r=row_data: self.open_edit_view(r))
#             self.room_table.setCellWidget(row, 9, edit_btn)

#     def open_edit_view(self, room_data):
#         dialog = EditRentalView(room_data, self)
#         if dialog.exec():
#             self.load_rooms()  # Refresh the table after editing

#     def filter_rooms(self, status):
#         all_rooms = fetch_room_details()
#         filtered_rooms = all_rooms if status == "All" else [room for room in all_rooms if room[7] == status]
#         self.room_table.setRowCount(0)
#         for row_data in filtered_rooms:
#             row = self.room_table.rowCount()
#             self.room_table.insertRow(row)
#             for col, data in enumerate(row_data):
#                 self.room_table.setItem(row, col, QTableWidgetItem(str(data)))

#             # Add Edit Button
#             edit_btn = QPushButton("Edit")
#             edit_btn.clicked.connect(lambda _, r=row_data: self.open_edit_view(r))
#             self.room_table.setCellWidget(row, 9, edit_btn)



from PyQt6.QtWidgets import QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QLabel
from views.edit_rental import EditRentalView
from controllers.rental_management_controller import fetch_room_details_with_booking


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
        self.room_table.setColumnCount(11)  # Adding a Booking Status column
        self.room_table.setHorizontalHeaderLabels([
            "ID", "Name", "Type", "Rental Price", "Payment Frequency", 
            "Security Deposit", "Grace Period", "Occupancy Status", 
            "Tenant", "Booking Status", "Actions"
        ])
        self.layout.addWidget(self.room_table)

        # Buttons
        self.refresh_btn = QPushButton("Refresh Rooms")
        self.refresh_btn.clicked.connect(self.load_rooms)
        self.layout.addWidget(self.refresh_btn)

        self.setLayout(self.layout)
        self.load_rooms()

    def load_rooms(self):
        # Fetch room details with booking info
        rooms = fetch_room_details_with_booking()
        self.room_table.setRowCount(0)
        for row_data in rooms:
            row = self.room_table.rowCount()
            self.room_table.insertRow(row)

            # Populate all columns except actions
            for col, data in enumerate(row_data[:-1]):
                self.room_table.setItem(row, col, QTableWidgetItem(str(data)))

            # Add Edit Button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, r=row_data: self.open_edit_view(r))
            self.room_table.setCellWidget(row, 10, edit_btn)

    def open_edit_view(self, room_data):
        dialog = EditRentalView(room_data, self)
        if dialog.exec():
            self.load_rooms()  # Refresh the table after editing

    def filter_rooms(self, status):
        all_rooms = fetch_room_details_with_booking()
        filtered_rooms = (
            all_rooms if status == "All" else 
            [room for room in all_rooms if (room[7] == status or (status == "Booked" and room[9] != "No Booking"))]
        )
        self.room_table.setRowCount(0)
        for row_data in filtered_rooms:
            row = self.room_table.rowCount()
            self.room_table.insertRow(row)

            # Populate all columns except actions
            for col, data in enumerate(row_data[:-1]):
                self.room_table.setItem(row, col, QTableWidgetItem(str(data)))

            # Add Edit Button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, r=row_data: self.open_edit_view(r))
            self.room_table.setCellWidget(row, 10, edit_btn)

