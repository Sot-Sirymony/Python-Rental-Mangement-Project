import sqlite3

import sqlite3

def add_property(name, address, description, amenities):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        INSERT INTO Property (name, address, description, amenities) VALUES (?, ?, ?, ?)
        """, (name, address, description, amenities))
        connection.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        raise
    finally:
        connection.close()
def add_room(property_id, name, room_type, size, rental_price, amenities):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        INSERT INTO Room (property_id, name, type, size, rental_price, amenities) VALUES (?, ?, ?, ?, ?, ?)
        """, (property_id, name, room_type, size, rental_price, amenities))
        connection.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        raise
    finally:
        connection.close()
def update_property(property_id, name, address, description, amenities):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE Property
    SET name = ?, address = ?, description = ?, amenities = ?
    WHERE id = ?
    """, (name, address, description, amenities, property_id))
    connection.commit()
    connection.close()    
def update_room(room_id, name, room_type, size, rental_price, amenities):
    connection = sqlite3.connect('rental_management.db')
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE Room
    SET name = ?, type = ?, size = ?, rental_price = ?, amenities = ?
    WHERE id = ?
    """, (name, room_type, size, rental_price, amenities, room_id))
    connection.commit()
    connection.close()

def delete_property(property_id):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Property WHERE id = ?", (property_id,))
    connection.commit()
    connection.close()
def delete_room(room_id):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Room WHERE id = ?", (room_id,))
    connection.commit()
    connection.close()
def fetch_properties():
    try:
        connection = sqlite3.connect('rental_management_v2.db')
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, address, description, amenities FROM Property")
        properties = cursor.fetchall()
        connection.close()
        return properties
    except Exception as e:
        print(f"Error fetching properties: {e}")
        return []
def open_edit_property_view(self, property_data):
    from views.edit_property import EditPropertyView
    current_data = {
        'name': property_data[1],
        'address': property_data[2],
        'description': property_data[3],  # Ensure description is now fetched
        'amenities': property_data[4]  # Ensure amenities are now fetched
    }
    self.edit_property_view = EditPropertyView(property_data[0], current_data)
    self.edit_property_view.show()
    
def fetch_rooms():
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT Room.id, Room.name, Property.name, Room.type, Room.size, Room.rental_price, Room.occupancy_status
    FROM Room
    JOIN Property ON Room.property_id = Property.id
    """)
    rooms = cursor.fetchall()
    connection.close()
    return rooms

def fetch_available_rooms():
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT id, name 
            FROM Room
            WHERE occupancy_status = 'Available'
        """)
        available_rooms = cursor.fetchall()
        return available_rooms
    except Exception as e:
        print(f"Error fetching available rooms: {e}")
        return []
    finally:
        connection.close()
        
def fetch_room_details_with_booking():
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        SELECT
            r.id, r.name, r.type, r.rental_price, r.payment_frequency, 
            r.security_deposit, r.grace_period, r.occupancy_status, 
            t.first_name || ' ' || t.last_name AS tenant_name,
            CASE
                WHEN b.status IS NULL THEN r.occupancy_status
                ELSE b.status
            END AS dynamic_status -- Dynamic status based on bookings
        FROM Room r
        LEFT JOIN Tenant t ON r.tenant_id = t.id
        LEFT JOIN (
            SELECT room_id, status
            FROM Booking
            WHERE status IN ('Pending', 'Active') -- Only consider relevant booking statuses
        ) b ON r.id = b.room_id;
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching room details with booking info: {e}")
        return []
    finally:
        connection.close()        


# def fetch_available_rooms():
#     connection = sqlite3.connect('rental_management_v2.db')
#     cursor = connection.cursor()
#     try:
#         cursor.execute("SELECT id, name FROM Room WHERE occupancy_status = 'Available'")
#         return cursor.fetchall()
#     except Exception as e:
#         print(f"Error fetching available rooms: {e}")
#         return []
#     finally:
#         connection.close()

        

