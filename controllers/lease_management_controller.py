
# from sqlite3 import connect
        
# def create_lease(room_id, tenant_id, start_date, end_date):
#     connection = connect('rental_management_v2.db')
#     cursor = connection.cursor()
#     try:
#         # Insert the lease
#         cursor.execute("""
#         INSERT INTO Lease (room_id, tenant_id, start_date, end_date)
#         VALUES (?, ?, ?, ?)
#         """, (room_id, tenant_id, start_date, end_date))
        
#         # Update the room's occupancy status
#         cursor.execute("""
#         UPDATE Room
#         SET occupancy_status = 'Rented', tenant_id = ?
#         WHERE id = ?
#         """, (tenant_id, room_id))
        
#         connection.commit()
#     except Exception as e:
#         print(f"Error creating lease: {e}")
#         raise
#     finally:
#         connection.close()
        
# def terminate_lease(lease_id):
#     connection = connect('rental_management_v2.db')
#     cursor = connection.cursor()
#     try:
#         # Fetch the room_id and tenant_id from the lease
#         cursor.execute("""
#         SELECT room_id FROM Lease WHERE id = ?
#         """, (lease_id,))
#         room_id = cursor.fetchone()[0]

#         # Update the lease status
#         cursor.execute("""
#         UPDATE Lease
#         SET status = 'Terminated'
#         WHERE id = ?
#         """, (lease_id,))

#         # Update the room's occupancy status
#         cursor.execute("""
#         UPDATE Room
#         SET occupancy_status = 'Available', tenant_id = NULL
#         WHERE id = ?
#         """, (room_id,))

#         connection.commit()
#     except Exception as e:
#         print(f"Error terminating lease: {e}")
#         raise
#     finally:
#         connection.close()
# def fetch_leases(room_id=None, tenant_id=None):
#     connection = connect('rental_management_v2.db')
#     cursor = connection.cursor()
#     try:
#         query = """
#         SELECT l.id, r.name AS room_name, t.first_name || ' ' || t.last_name AS tenant_name,
#                l.start_date, l.end_date, l.status
#         FROM Lease l
#         JOIN Room r ON l.room_id = r.id
#         JOIN Tenant t ON l.tenant_id = t.id
#         WHERE 1=1
#         """
#         params = []
#         if room_id:
#             query += " AND l.room_id = ?"
#             params.append(room_id)
#         if tenant_id:
#             query += " AND l.tenant_id = ?"
#             params.append(tenant_id)
        
#         cursor.execute(query, params)
#         return cursor.fetchall()
#     except Exception as e:
#         print(f"Error fetching leases: {e}")
#         return []
#     finally:
#         connection.close()
        
# def update_lease(lease_id, start_date, end_date, status):
#     connection = connect('rental_management_v2.db')
#     cursor = connection.cursor()
#     try:
#         cursor.execute("""
#         UPDATE Lease
#         SET start_date = ?, end_date = ?, status = ?
#         WHERE id = ?
#         """, (start_date, end_date, status, lease_id))
#         connection.commit()
#     except Exception as e:
#         print(f"Error updating lease: {e}")
#         raise
#     finally:
#         connection.close()


# File: controllers/lease_management_controller.py
from sqlite3 import connect

def create_lease(room_id, tenant_id, start_date, end_date):
    """Create a lease and update the room's occupancy status."""
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        # Check if room exists
        cursor.execute("SELECT id FROM Room WHERE id = ?", (room_id,))
        if not cursor.fetchone():
            raise ValueError(f"Room ID {room_id} does not exist.")

        # Check if tenant exists
        cursor.execute("SELECT id FROM Tenant WHERE id = ?", (tenant_id,))
        if not cursor.fetchone():
            raise ValueError(f"Tenant ID {tenant_id} does not exist.")

        # Insert the lease
        cursor.execute("""
        INSERT INTO Lease (room_id, tenant_id, start_date, end_date)
        VALUES (?, ?, ?, ?)
        """, (room_id, tenant_id, start_date, end_date))

        # Update the room's occupancy status
        cursor.execute("""
        UPDATE Room
        SET occupancy_status = 'Rented', tenant_id = ?
        WHERE id = ?
        """, (tenant_id, room_id))

        connection.commit()
        print(f"Lease created successfully for Room ID {room_id} and Tenant ID {tenant_id}.")
    except Exception as e:
        print(f"Error creating lease: {e}")
        raise
    finally:
        connection.close()

def terminate_lease(lease_id):
    """Terminate a lease and update the room's occupancy status."""
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        # Fetch the room_id from the lease
        cursor.execute("SELECT room_id FROM Lease WHERE id = ?", (lease_id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Lease ID {lease_id} does not exist.")
        room_id = row[0]

        # Update the lease status
        cursor.execute("""
        UPDATE Lease
        SET status = 'Terminated'
        WHERE id = ?
        """, (lease_id,))

        # Update the room's occupancy status
        cursor.execute("""
        UPDATE Room
        SET occupancy_status = 'Available', tenant_id = NULL
        WHERE id = ?
        """, (room_id,))

        connection.commit()
        print(f"Lease ID {lease_id} terminated successfully.")
    except Exception as e:
        print(f"Error terminating lease: {e}")
        raise
    finally:
        connection.close()

def fetch_leases(room_id=None, tenant_id=None):
    """Fetch lease details with optional filters for room or tenant."""
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        query = """
        SELECT l.id, r.name AS room_name, t.first_name || ' ' || t.last_name AS tenant_name,
               l.start_date, l.end_date, l.status
        FROM Lease l
        JOIN Room r ON l.room_id = r.id
        JOIN Tenant t ON l.tenant_id = t.id
        WHERE 1=1
        """
        params = []
        if room_id:
            query += " AND l.room_id = ?"
            params.append(room_id)
        if tenant_id:
            query += " AND l.tenant_id = ?"
            params.append(tenant_id)
        
        cursor.execute(query, params)
        leases = cursor.fetchall()
        print(f"Fetched {len(leases)} lease(s).")
        return leases
    except Exception as e:
        print(f"Error fetching leases: {e}")
        return []
    finally:
        connection.close()

def update_lease(lease_id, start_date=None, end_date=None, status=None):
    """Update lease details such as start date, end date, or status."""
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        # Build dynamic query
        fields_to_update = []
        params = []

        if start_date:
            fields_to_update.append("start_date = ?")
            params.append(start_date)
        if end_date:
            fields_to_update.append("end_date = ?")
            params.append(end_date)
        if status:
            fields_to_update.append("status = ?")
            params.append(status)

        if not fields_to_update:
            raise ValueError("No fields provided for update.")

        params.append(lease_id)
        query = f"UPDATE Lease SET {', '.join(fields_to_update)} WHERE id = ?"

        cursor.execute(query, params)
        connection.commit()
        print(f"Lease ID {lease_id} updated successfully.")
    except Exception as e:
        print(f"Error updating lease: {e}")
        raise
    finally:
        connection.close()

       
        
        
     
