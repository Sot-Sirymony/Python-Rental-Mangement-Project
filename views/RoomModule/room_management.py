
from PyQt6.QtWidgets import (
    QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
    QWidget, QMessageBox, QHBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from functools import partial
from controllers.PostGreSqlControllers.room_controller import fetch_rooms


class RoomManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Room Management")
        self.layout = QVBoxLayout()

        # Room Table
        self.room_table = QTableWidget()
        self.room_table.setColumnCount(8)  # Updated for separate Edit and Delete columns
        self.room_table.setHorizontalHeaderLabels([
            "Room ID", "Room Name", "Room Type", "Room Size", "Rental Price",
            "Occupancy Status", "Action Edit", "Action Delete"
        ])
        
        # Adjust column width for each column
        self.room_table.setColumnWidth(0, 100)  # Room ID
        self.room_table.setColumnWidth(1, 240)  # Room Name
        self.room_table.setColumnWidth(2, 150)  # Room Type
        self.room_table.setColumnWidth(3, 120)  # Room Size
        self.room_table.setColumnWidth(4, 170)  # Rental Price
        self.room_table.setColumnWidth(5, 180)  # Occupancy Status
        self.room_table.setColumnWidth(6, 120)  # Action Edit
        self.room_table.setColumnWidth(7, 120)  # Action Delete

        # Apply table styling
        self.room_table.setStyleSheet(
            """
            QTableWidget::item { text-align: center; }
            QHeaderView::section { font-size: 16px; font-weight: bold; text-align: center; }
            """
        )

        # Enable horizontal scrolling
        self.room_table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.room_table.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
        self.room_table.horizontalScrollBar().setVisible(True)

        # Adjust column width and row height
        self.room_table.horizontalHeader().setDefaultSectionSize(150)  # Set default width for columns
        self.room_table.verticalHeader().setDefaultSectionSize(40)  # Set default height for rows
        self.room_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)  # Allow column resizing

        self.layout.addWidget(self.room_table)

        # Buttons
        button_layout = QHBoxLayout()

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setStyleSheet("font-size: 14px; font-weight:bold; padding: 10px;")
        self.refresh_btn.clicked.connect(self.load_rooms)
        button_layout.addWidget(self.refresh_btn)

        self.add_room_btn = QPushButton("Add Room")
        self.add_room_btn.setStyleSheet("font-size: 14px;font-weight:bold; padding: 10px;")
        self.add_room_btn.clicked.connect(self.open_add_room_view)
        button_layout.addWidget(self.add_room_btn)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        self.load_rooms()

    def load_rooms(self):
        """Fetch and display all rooms."""
        try:
            rooms = fetch_rooms()
            if not rooms:
                QMessageBox.information(self, "Info", "No rooms found.")
                self.room_table.setRowCount(0)  # Clear any existing rows
                return
            self.populate_table(rooms)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load rooms: {e}")

    def populate_table(self, rooms):
        """Populate the table with room data."""
        self.room_table.setRowCount(0)  # Clear existing rows

        # Set font for table rows
        row_font = QFont()
        row_font.setPointSize(14)  # Set font size for row values

        for row_data in rooms:
            row = self.room_table.rowCount()
            self.room_table.insertRow(row)

            # Populate all columns with room data (excluding actions)
            for col, data in enumerate(row_data[:6]):
                item = QTableWidgetItem(str(data) if data is not None else "N/A")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align text
                item.setFont(row_font)  # Apply the font to the row item
                self.room_table.setItem(row, col, item)

            # Add action buttons
            self.add_edit_action(row, row_data)
            self.add_delete_action(row, row_data)

    def add_edit_action(self, row, row_data):
        """Add the Edit button to the table."""
        edit_btn = QPushButton("Edit Room")
        edit_btn.setStyleSheet("font-size: 14px;font-weight:bold; padding: 5px;")
        edit_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        edit_btn.clicked.connect(partial(self.open_edit_room_view, row_data))
        self.room_table.setCellWidget(row, 6, edit_btn)  # Place in the "Action Edit" column

    def add_delete_action(self, row, row_data):
        """Add the Delete button to the table."""
        delete_btn = QPushButton("Delete Room")
        delete_btn.setStyleSheet("font-size: 14px; font-weight:bold; padding: 5px;")
        delete_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        delete_btn.clicked.connect(partial(self.delete_room_action, row_data[0]))
        self.room_table.setCellWidget(row, 7, delete_btn)  # Place in the "Action Delete" column

    def delete_room_action(self, room_id):
        """Delete a room."""
        from controllers.PostGreSqlControllers.room_controller import delete_room
        try:
            delete_room(room_id)
            QMessageBox.information(self, "Success", f"Room ID {room_id} deleted successfully!")
            self.load_rooms()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete Room ID {room_id}: {e}")
    
    def open_edit_room_view(self, room_data):
        """Open the edit room dialog."""
        current_data = {
            'name': str(room_data[1]),  # Room Name
            'type': str(room_data[2]),  # Room Type
            'size': str(room_data[3]),  # Room Size
            'rental_price': str(room_data[4]),  # Rental Price
            'amenities': str(room_data[6]) if len(room_data) > 6 else ""  # Amenities
        }
        from views.RoomModule.edit_room import EditRoomView
        dialog = EditRoomView(room_data[0], current_data)  # Pass Room ID and current data
        if dialog.exec():
            self.load_rooms()  # Reload rooms after editing


    def open_add_room_view(self):
        """Open the add room dialog."""
        from views.RoomModule.add_room import AddRoomView
        dialog = AddRoomView(self)
        if dialog.exec():
            self.load_rooms()


