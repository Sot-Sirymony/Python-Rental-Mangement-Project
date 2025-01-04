import psycopg2
import pandas as pd

DATABASE = {
    'dbname': 'rental_management_db',
    'user': 'postgres',
    'password': 'Mony@1144',
    'host': 'localhost',
    'port': 5432
}

# def get_connection():
#     return psycopg2.connect(**DATABASE)
def get_connection():
    try:
        connection = psycopg2.connect(**DATABASE)
        print("Connection successful!")
        return connection  # Return the open connection
    except Exception as e:
        print(f"Connection failed: {e}")
        return None  # Return None if the connection fails

def add_room(name, room_type, size, rental_price, amenities):
    """Add a new room."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT add_room(%s, %s, %s, %s, %s);",
                       (name, room_type, size, rental_price, amenities))
        connection.commit()
    except Exception as e:
        print(f"Error adding room: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def update_room(room_id, name, room_type, size, rental_price, amenities, occupancy_status):
    """Update an existing room."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT update_room(%s, %s, %s, %s, %s, %s, %s);",
                       (room_id, name, room_type, size, rental_price, amenities, occupancy_status))
        connection.commit()
    except Exception as e:
        print(f"Error updating room: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def delete_room(room_id):
    """Delete a room."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT delete_room(%s);", (room_id,))
        connection.commit()
    except Exception as e:
        print(f"Error deleting room: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def fetch_rooms():
    """Fetch all room details."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM Room;")
        rooms = cursor.fetchall()
        return rooms
    except Exception as e:
        print(f"Error fetching rooms: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def fetch_available_rooms():
    """Fetch available rooms."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM AvailableRooms;")
        available_rooms = cursor.fetchall()
        return available_rooms
    except Exception as e:
        print(f"Error fetching available rooms: {e}")
        return []
    finally:
        cursor.close()
        connection.close()
