

from PyQt6.QtWidgets import (
    QVBoxLayout, QPushButton, QLabel, QWidget, QTableWidget, QTableWidgetItem, QHeaderView
)
from functools import partial


class RoomManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Rooms Management"))

        self.room_table = QTableWidget()

        # Buttons for room management
        self.add_room_btn = QPushButton("Add Room")
        self.add_room_btn.clicked.connect(self.open_add_room_view)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_data)  # Reload room data

        for widget in [self.room_table, self.add_room_btn, self.refresh_btn]:
            self.layout.addWidget(widget)

        self.setLayout(self.layout)
        self.load_rooms()

    def refresh_data(self):
        """Reload room data."""
        self.load_rooms()

    def load_rooms(self):
        from controllers.room_controller import fetch_rooms  # Updated controller for fetching rooms
        rooms = fetch_rooms()  # Fetch room data from the controller

        # Begin smooth table update
        self.room_table.setUpdatesEnabled(False)
        self.room_table.clearContents()
        self.room_table.setRowCount(0)

        # Set the correct column headers, including Edit and Delete actions
        self.room_table.setColumnCount(7)  # Adjusted for Edit and Delete columns
        self.room_table.setHorizontalHeaderLabels(
            ["ID", "Room Name", "Room Type", "Room Size", "Rental Price", "Occupancy Status", "Actions"]
        )

        # Populate table
        for row_data in rooms:
            row = self.room_table.rowCount()
            self.room_table.insertRow(row)

            # Map each value from `row_data` to its corresponding column
            for col, data in enumerate(row_data[:6]):  # Ensure only the first 6 columns are populated
                self.room_table.setItem(row, col, QTableWidgetItem(str(data)))

            # Add Edit and Delete buttons in the Actions column
            actions_widget = QWidget()
            actions_layout = QVBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)

            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(partial(self.open_edit_room_view, row_data))
            actions_layout.addWidget(edit_btn)

            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(partial(self.delete_room_action, row_data[0]))
            actions_layout.addWidget(delete_btn)

            actions_widget.setLayout(actions_layout)
            self.room_table.setCellWidget(row, 6, actions_widget)

        # Resize columns to fit content
        self.room_table.resizeColumnsToContents()

        # Re-enable updates
        self.room_table.setUpdatesEnabled(True)

    def delete_room_action(self, room_id):
        from controllers.room_controller import delete_room
        try:
            # Call the controller to delete the room
            delete_room(room_id)
            print(f"Room ID {room_id} deleted successfully!")
            self.load_rooms()  # Refresh table after deletion
        except Exception as e:
            print(f"Failed to delete Room ID {room_id}: {e}")

    def open_edit_room_view(self, room_data):
        from views.edit_room import EditRoomView
        current_data = {
            'name': str(room_data[1]),
            'type': str(room_data[2]),
            'size': str(room_data[3]),
            'rental_price': str(room_data[4]),
            'occupancy_status': str(room_data[5])
        }
        self.edit_room_view = EditRoomView(room_data[0], current_data)
        self.edit_room_view.show()

    def open_add_room_view(self):
        from views.add_room import AddRoomView
        self.add_room_view = AddRoomView()
        self.add_room_view.show()
