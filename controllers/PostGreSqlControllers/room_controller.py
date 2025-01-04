

import sqlite3
import pandas as pd
DATABASE = "rental_management_v2.db"

def add_room(name, room_type, size, rental_price, amenities):
    """Add a new room."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        cursor.execute("""
        INSERT INTO Room (name, type, size, rental_price, amenities)
        VALUES (?, ?, ?, ?, ?)
        """, (name, room_type, size, rental_price, amenities))
        connection.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error adding room: {e}")
        raise
    finally:
        connection.close()


def update_room(room_id, name, room_type, size, rental_price, amenities, occupancy_status):
    connection = sqlite3.connect(DATABASE)  # Replace with your database file name
    cursor = connection.cursor()
    try:
        # Update query to include `occupancy_status`
        cursor.execute("""
        UPDATE Room
        SET name = ?, type = ?, size = ?, rental_price = ?, amenities = ?, occupancy_status = ?
        WHERE id = ?;
        """, (name, room_type, size, rental_price, amenities, occupancy_status, room_id))
        connection.commit()
    except Exception as e:
        print(f"Error updating room: {e}")
        raise
    finally:
        connection.close()

def delete_room(room_id):
    """Delete a room."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Room WHERE id = ?", (room_id,))
        connection.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error deleting room: {e}")
        raise
    finally:
        connection.close()


def fetch_rooms():
    """Fetch all room details."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        cursor.execute("""
        SELECT
            id, name, type, size, rental_price, occupancy_status, amenities
        FROM Room
        """)
        rooms = cursor.fetchall()
        return rooms
    except Exception as e:
        print(f"Error fetching rooms: {e}")
        return []
    finally:
        connection.close()


def fetch_available_rooms():
    """Fetch available rooms."""
    connection = sqlite3.connect(DATABASE)
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
    """Fetch room details with booking information."""
    connection = sqlite3.connect(DATABASE)
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
        ) b ON r.id = b.room_id
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching room details with booking info: {e}")
        return []
    finally:
        connection.close()
        
        
def fetch_room_data():
    """Fetch detailed room data for the Payment Report."""
    connection = sqlite3.connect(DATABASE)
    try:
        query = """
        SELECT 
            r.id AS room_id,
            r.name AS room_name,
            r.type AS room_type,
            r.rental_price,
            r.occupancy_status,
            r.size AS room_size,
            r.amenities,
            (SELECT SUM(p.amount) 
             FROM Payment p 
             WHERE p.room_id = r.id) AS total_rent_collected,
            (SELECT COUNT(*) 
             FROM Lease l 
             WHERE l.room_id = r.id AND l.status = 'Active') AS active_lease_count,
            (SELECT COUNT(*) 
             FROM Payment p 
             WHERE p.room_id = r.id AND p.payment_status = 'Overdue') AS overdue_payments
        FROM Room r
        """
        df = pd.read_sql_query(query, connection)
        return df
    except Exception as e:
        print(f"Error fetching room data for report: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    finally:
        connection.close()        


        

