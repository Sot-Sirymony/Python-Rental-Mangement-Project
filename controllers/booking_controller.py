import sqlite3
def add_booking(room_id, tenant_id, start_date, end_date, notes, status="Pending"):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        # Check for overlapping bookings
        cursor.execute("""
        SELECT COUNT(*) FROM Booking
        WHERE room_id = ? AND status IN ('Pending', 'Active')
        AND (start_date <= ? AND end_date >= ?)
        """, (room_id, end_date, start_date))
        if cursor.fetchone()[0] > 0:
            raise ValueError("Room is already booked during the selected period.")

        # Insert new booking
        cursor.execute("""
        INSERT INTO Booking (room_id, tenant_id, start_date, end_date, notes, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (room_id, tenant_id, start_date, end_date, notes, status))
        connection.commit()
    except Exception as e:
        print(f"Error adding booking: {e}")
        raise
    finally:
        connection.close()
def fetch_bookings():
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        SELECT b.id, r.name AS room_name, 
               t.first_name || ' ' || t.last_name AS tenant_name, 
               b.start_date, b.end_date, b.status,b.notes
        FROM Booking b
        JOIN Room r ON b.room_id = r.id
        JOIN Tenant t ON b.tenant_id = t.id;
        """)
        bookings = cursor.fetchall()
        return bookings
    except Exception as e:
        print(f"Error fetching bookings: {e}")
        return []
    finally:
        connection.close()
        
        
def delete_booking(booking_id):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Booking WHERE id = ?", (booking_id,))
        connection.commit()
    except Exception as e:
        print(f"Error deleting booking: {e}")
        raise
    finally:
        connection.close()  

import sqlite3

def update_booking(booking_id, room_id, tenant_id, start_date, end_date, notes, status):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        # Update query to include notes and status
        cursor.execute("""
        UPDATE Booking
        SET room_id = ?, tenant_id = ?, start_date = ?, end_date = ?, notes = ?, status = ?
        WHERE id = ?
        """, (room_id, tenant_id, start_date, end_date, notes, status, booking_id))
        connection.commit()
    except Exception as e:
        print(f"Error updating booking: {e}")
        raise
    finally:
        connection.close()

        
def confirm_booking(booking_id, room_id):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE Booking SET status = 'Active' WHERE id = ?", (booking_id,))
        cursor.execute("UPDATE Room SET occupancy_status = 'Rented' WHERE id = ?", (room_id,))
        connection.commit()
    except Exception as e:
        print(f"Error confirming booking: {e}")
    finally:
        connection.close()   
        
def cancel_booking(booking_id, room_id):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE Booking SET status = 'Canceled' WHERE id = ?", (booking_id,))
        cursor.execute("UPDATE Room SET occupancy_status = 'Available' WHERE id = ?", (room_id,))
        connection.commit()
    except Exception as e:
        print(f"Error canceling booking: {e}")
    finally:
        connection.close()
             
