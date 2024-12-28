#from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QWidget, QTableWidget, QTableWidgetItem
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QWidget, QTableWidget, QTableWidgetItem, QHeaderView

from PyQt6.QtWidgets import QPushButton
from controllers.property_controller import fetch_properties
from functools import partial

class PropertyRoomManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Properties & Rooms Management"))

        self.property_table = QTableWidget()
        self.room_table = QTableWidget()

        self.add_property_btn = QPushButton("Add Property")
        self.add_property_btn.clicked.connect(self.open_add_property_view)

        self.add_room_btn = QPushButton("Add Room")
        self.add_room_btn.clicked.connect(self.open_add_room_view)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_data)  # Connect refresh button to reload both properties and rooms

        for widget in [self.property_table, self.room_table, self.add_property_btn, self.add_room_btn,self.refresh_btn]:
            self.layout.addWidget(widget)

        self.setLayout(self.layout)
        self.load_properties()
        self.load_rooms()
    # def load_properties(self):
    # # Fetch updated property data
    #     properties = fetch_properties()

    #     # Begin smooth table update
    #     self.property_table.setUpdatesEnabled(False)  # Disable updates to avoid flickering
    #     self.property_table.clearContents()  # Clear existing table contents
    #     self.property_table.setRowCount(0)  # Reset row count

    #     # Configure columns
    #     self.property_table.setColumnCount(6)  # Increased column count to 6
    #     self.property_table.setHorizontalHeaderLabels(["ID", "Name", "Address", "Description", "Edit", "Delete"])  # Updated headers

    #     # Populate table with new data
    #     for row_data in properties:
    #         row = self.property_table.rowCount()
    #         self.property_table.insertRow(row)

    #         # Fill columns with data (ID, Name, Address, Description)
    #         for col, data in enumerate(row_data):
    #             self.property_table.setItem(row, col, QTableWidgetItem(str(data)))

    #         # Add "Edit" button to the "Edit" column
    #         edit_btn = QPushButton("Edit")
    #         edit_btn.clicked.connect(partial(self.open_edit_property_view, row_data))
    #         self.property_table.setCellWidget(row, 4, edit_btn)  # Edit column index is 4

    #         # Add "Delete" button to the "Delete" column
    #         delete_btn = QPushButton("Delete")
    #         delete_btn.clicked.connect(partial(self.delete_property_action, row_data[0]))
    #         self.property_table.setCellWidget(row, 5, delete_btn)  # Delete column index is 5

    #     # Resize columns to fit content
    #     self.property_table.resizeColumnsToContents()

    #     # Re-enable updates
    #     self.property_table.setUpdatesEnabled(True)
    
    def load_properties(self):
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QAbstractScrollArea

        # Fetch updated property data
        properties = fetch_properties()

        # Begin smooth table update
        self.property_table.setUpdatesEnabled(False)
        self.property_table.clearContents()
        self.property_table.setRowCount(0)

        # Configure columns
        self.property_table.setColumnCount(6)
        self.property_table.setHorizontalHeaderLabels(["ID", "Name", "Address", "Description", "Edit", "Delete"])

        # Set horizontal header behavior
        self.property_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.property_table.horizontalHeader().setStretchLastSection(False)
        self.property_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

        # Populate table with new data
        for row_data in properties:
            row = self.property_table.rowCount()
            self.property_table.insertRow(row)

            # Fill columns with data (ID, Name, Address, Description)
            for col, data in enumerate(row_data):
                self.property_table.setItem(row, col, QTableWidgetItem(str(data)))

            # Add "Edit" button to the "Edit" column
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(partial(self.open_edit_property_view, row_data))
            self.property_table.setCellWidget(row, 4, edit_btn)

            # Add "Delete" button to the "Delete" column
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(partial(self.delete_property_action, row_data[0]))
            self.property_table.setCellWidget(row, 5, delete_btn)

        # Resize columns to fit content and enable horizontal scrolling
        self.property_table.resizeColumnsToContents()
        self.property_table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.property_table.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)

        # Re-enable updates
        self.property_table.setUpdatesEnabled(True)




    def delete_property_action(self, property_id):
        from controllers.property_controller import delete_property
        try:
            delete_property(property_id)
            print(f"Property ID {property_id} deleted successfully!")
            self.load_properties()  # Refresh table after deletion
        except Exception as e:
            print(f"Failed to delete property ID {property_id}: {e}")
        
    def refresh_data(self):
        """Reload both properties and rooms."""
        self.load_properties()
        self.load_rooms()    

    # def load_rooms(self):
    #     from controllers.property_controller import fetch_rooms
    #     rooms = fetch_rooms()  # Fetch room data from the controller

    #     # Begin smooth table update
    #     self.room_table.setUpdatesEnabled(False)
    #     self.room_table.clearContents()
    #     self.room_table.setRowCount(0)

    #     # Set the correct column headers, including Edit and Delete actions
    #     self.room_table.setColumnCount(9)  # Adjusted for Edit and Delete columns
    #     self.room_table.setHorizontalHeaderLabels(
    #         ["ID", "Room Name", "Property Name", "Room Type", "Room Size", "Rental Price", "Occupancy Status", "Edit", "Delete"]
    #     )

    #     # Populate table
    #     for row_data in rooms:
    #         row = self.room_table.rowCount()
    #         self.room_table.insertRow(row)

    #         # Map each value from `row_data` to its corresponding column
    #         for col, data in enumerate(row_data[:7]):  # Ensure only the first 7 columns are populated
    #             self.room_table.setItem(row, col, QTableWidgetItem(str(data)))

    #         # Add Edit button
    #         edit_btn = QPushButton("Edit")
    #         edit_btn.clicked.connect(lambda _, r=row_data: self.open_edit_room_view(r))
    #         self.room_table.setCellWidget(row, 7, edit_btn)  # Edit column index is 7

    #         # Add Delete button
    #         delete_btn = QPushButton("Delete")
    #         delete_btn.clicked.connect(lambda _, r=row_data: self.delete_room_action(r[0]))  # Pass Room ID to delete function
    #         self.room_table.setCellWidget(row, 8, delete_btn)  # Delete column index is 8

    #     # Re-enable updates
    #     self.room_table.setUpdatesEnabled(True)
    
    def load_rooms(self):
        from controllers.property_controller import fetch_rooms
        rooms = fetch_rooms()  # Fetch room data from the controller

        # Begin smooth table update
        self.room_table.setUpdatesEnabled(False)
        self.room_table.clearContents()
        self.room_table.setRowCount(0)

        # Set the correct column headers, including Edit and Delete actions
        self.room_table.setColumnCount(9)  # Adjusted for Edit and Delete columns
        self.room_table.setHorizontalHeaderLabels(
            ["ID", "Room Name", "Property Name", "Room Type", "Room Size", "Rental Price", "Occupancy Status", "Edit", "Delete"]
        )

        # Populate table
        for row_data in rooms:
            row = self.room_table.rowCount()
            self.room_table.insertRow(row)

            # Map each value from `row_data` to its corresponding column
            for col, data in enumerate(row_data[:7]):  # Ensure only the first 7 columns are populated
                self.room_table.setItem(row, col, QTableWidgetItem(str(data)))

            # Add Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, r=row_data: self.open_edit_room_view(r))
            self.room_table.setCellWidget(row, 7, edit_btn)  # Edit column index is 7

            # Add Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda _, r=row_data: self.delete_room_action(r[0]))  # Pass Room ID to delete function
            self.room_table.setCellWidget(row, 8, delete_btn)  # Delete column index is 8

        # Resize columns to fit content
        self.room_table.resizeColumnsToContents()

        # Re-enable updates
        self.room_table.setUpdatesEnabled(True)

    def delete_room_action(self, room_id):
        from controllers.property_controller import delete_room
        try:
            # Call the controller to delete the room
            delete_room(room_id)
            print(f"Room ID {room_id} deleted successfully!")
            self.load_rooms()  # Refresh table after deletion
        except Exception as e:
            print(f"Failed to delete Room ID {room_id}: {e}")

    def open_edit_property_view(self, property_data):
        from views.edit_property import EditPropertyView
        current_data = {
            'name': property_data[1],
            'address': property_data[2],
            'description': property_data[3],
            'amenities': property_data[4]
        }
        self.edit_property_view = EditPropertyView(property_data[0], current_data)
        self.edit_property_view.show()
    def open_edit_room_view(self, room_data):
        from views.edit_room import EditRoomView
        current_data = {
            'name': str(room_data[1]),
            'type': str(room_data[2]),
            'size': str(room_data[3]),
            'rental_price': str(room_data[4]),
            'amenities': str(room_data[5])  # Convert amenities to string
        }
        self.edit_room_view = EditRoomView(room_data[0], current_data)
        self.edit_room_view.show()
        

    def open_add_property_view(self):
        from views.add_property import AddPropertyView
        self.add_property_view = AddPropertyView()
        self.add_property_view.show()

    def open_add_room_view(self):
        from views.add_room import AddRoomView
        self.add_room_view = AddRoomView()
        self.add_room_view.show()
