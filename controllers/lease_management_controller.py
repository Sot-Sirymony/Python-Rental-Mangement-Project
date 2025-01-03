import sqlite3

DATABASE = "rental_management_v2.db"

def fetch_leases():
    """Fetch all leases."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        cursor.execute("""
        SELECT l.id AS lease_id, r.name AS room_name, t.first_name || ' ' || t.last_name AS tenant_name,
               l.start_date, l.end_date, l.status
        FROM Lease l
        JOIN Room r ON l.room_id = r.id
        JOIN Tenant t ON l.tenant_id = t.id
        ORDER BY l.start_date DESC
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching leases: {e}")
        return []
    finally:
        connection.close()

def cancel_lease(lease_id):
    """Cancel a lease and update the room's status."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        # Update lease status to "Canceled"
        cursor.execute("""
        UPDATE Lease
        SET status = 'Canceled'
        WHERE id = ?
        """, (lease_id,))

        # Set the associated room's occupancy status to "Available"
        cursor.execute("""
        UPDATE Room
        SET occupancy_status = 'Available'
        WHERE id = (SELECT room_id FROM Lease WHERE id = ?)
        """, (lease_id,))
        connection.commit()
    except Exception as e:
        print(f"Error canceling lease: {e}")
        raise
    finally:
        connection.close()

def delete_lease(lease_id):
    """Delete a lease."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Lease WHERE id = ?", (lease_id,))
        connection.commit()
    except Exception as e:
        print(f"Error deleting lease: {e}")
        raise
    finally:
        connection.close()
        
def fetch_available_rooms():
    """Fetch all available rooms."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        cursor.execute("""
        SELECT id, name FROM Room WHERE occupancy_status = 'Available'
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching available rooms: {e}")
        return []
    finally:
        connection.close()

def fetch_tenants():
    """Fetch all tenants."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        cursor.execute("""
        SELECT id, first_name || ' ' || last_name AS name FROM Tenant
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching tenants: {e}")
        return []
    finally:
        connection.close()

def create_lease(room_id, tenant_id, start_date, end_date):
    """Create a new lease."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        # Check for overlapping leases
        cursor.execute("""
        SELECT COUNT(*) FROM Lease
        WHERE room_id = ? AND status = 'Active'
        AND (start_date BETWEEN ? AND ? OR end_date BETWEEN ? AND ?)
        """, (room_id, start_date, end_date, start_date, end_date))
        if cursor.fetchone()[0] > 0:
            raise Exception("This room already has an active lease in the selected period.")

        # Insert lease and update room status
        cursor.execute("""
        INSERT INTO Lease (room_id, tenant_id, start_date, end_date, status)
        VALUES (?, ?, ?, ?, 'Active')
        """, (room_id, tenant_id, start_date, end_date))
        cursor.execute("""
        UPDATE Room SET occupancy_status = 'Rented' WHERE id = ?
        """, (room_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error creating lease: {e}")
        raise
    finally:
        connection.close()     
        
def update_lease(lease_id, start_date, end_date, status):
    """Update lease details and handle automatic updates."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        # Update lease details
        cursor.execute("""
        UPDATE Lease
        SET start_date = ?, end_date = ?, status = ?
        WHERE id = ?
        """, (start_date, end_date, status, lease_id))

        # Handle automatic updates for room status
        if status == "Completed":
            cursor.execute("""
            UPDATE Room
            SET occupancy_status = 'Available'
            WHERE id = (SELECT room_id FROM Lease WHERE id = ?)
            """, (lease_id,))
        elif status == "Canceled":
            cursor.execute("""
            UPDATE Room
            SET occupancy_status = 'Available'
            WHERE id = (SELECT room_id FROM Lease WHERE id = ?)
            """, (lease_id,))
        elif status == "Active":
            cursor.execute("""
            UPDATE Room
            SET occupancy_status = 'Rented'
            WHERE id = (SELECT room_id FROM Lease WHERE id = ?)
            """, (lease_id,))    

        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error updating lease: {e}")
        raise
    finally:
        connection.close()
        
           
        
        
        
        
