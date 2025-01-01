

import sqlite3

def add_payment(tenant, room, amount, date, method, reference=None, due_date=None, payment_status="Pending", notes=None):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        tenant_id = _get_tenant_id(cursor, tenant)
        room_id = _get_room_id(cursor, room)

        # Validate due_date and payment_date
        if due_date and due_date < date:
            raise ValueError("Due date must be after the payment date.")

        cursor.execute("""
        INSERT INTO Payment (tenant_id, room_id, amount, date, method, reference_number, due_date, payment_status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (tenant_id, room_id, amount, date, method, reference, due_date, payment_status, notes))
        connection.commit()
        print("Payment added successfully!")
    except Exception as e:
        print(f"Error adding payment: {e}")
        raise
    finally:
        connection.close()

def update_payment(payment_id, amount, method, payment_date, due_date, reference, payment_status):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        if due_date and payment_date and due_date < payment_date:
            raise ValueError("Due date must be after the payment date.")

        cursor.execute("""
        UPDATE Payment
        SET amount = ?,
            method = ?,
            date = ?,
            due_date = ?,
            reference_number = ?,
            payment_status = ?
        WHERE id = ?
        """, (amount, method, payment_date, due_date, reference, payment_status, payment_id))
        connection.commit()
        print("Payment updated successfully!")
    except Exception as e:
        print(f"Error updating payment: {e}")
        raise
    finally:
        connection.close()

def _get_tenant_id(cursor, tenant):
    tenant_str = str(tenant)
    if tenant_str.isdigit():
        cursor.execute("SELECT id FROM Tenant WHERE id = ?", (int(tenant_str),))
    else:
        cursor.execute("SELECT id FROM Tenant WHERE first_name || ' ' || last_name = ?", (tenant_str,))
    result = cursor.fetchone()
    if not result:
        raise ValueError(f"Tenant '{tenant}' not found in the database.")
    return result[0]

def _get_room_id(cursor, room):
    room_str = str(room)
    if room_str.isdigit():
        cursor.execute("SELECT id FROM Room WHERE id = ?", (int(room_str),))
    else:
        cursor.execute("SELECT id FROM Room WHERE name = ?", (room_str,))
    result = cursor.fetchone()
    if not result:
        raise ValueError(f"Room '{room}' not found in the database.")
    return result[0]

def fetch_payment_methods():
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT DISTINCT method FROM Payment WHERE method IS NOT NULL")
        return [row[0] for row in cursor.fetchall()]
    finally:
        connection.close()

def fetch_payment_history(tenant_id=None, room_id=None, method=None, start_date=None, end_date=None):
    """
    Fetch payment history with optional filters for tenant, room, method, and date range.
    """
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        # Query to fetch payment data with tenant and room details
        query = """
        SELECT p.id, 
               t.first_name || ' ' || t.last_name AS tenant_name, 
               r.name AS room_name, 
               p.amount, 
               p.method, 
               p.date, 
               p.due_date, 
               p.payment_status, 
               p.reference_number, 
               p.notes
        FROM Payment p
        JOIN Tenant t ON p.tenant_id = t.id
        JOIN Room r ON p.room_id = r.id
        WHERE 1=1
        """
        params = []
        # Apply filters dynamically
        if tenant_id:
            query += " AND p.tenant_id = ?"
            params.append(tenant_id)
        if room_id:
            query += " AND p.room_id = ?"
            params.append(room_id)
        if method:
            query += " AND p.method = ?"
            params.append(method)
        if start_date:
            query += " AND p.date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND p.date <= ?"
            params.append(end_date)

        # Execute query
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching payment history: {e}")
        return []
    finally:
        connection.close()
def delete_payment(payment_id):
    """
    Delete a payment record by its ID.
    """
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        # Delete payment record
        cursor.execute("DELETE FROM Payment WHERE id = ?", (payment_id,))
        connection.commit()
        print(f"Payment with ID {payment_id} deleted successfully!")
    except Exception as e:
        print(f"Error deleting payment: {e}")
        raise
    finally:
        connection.close()
def fetch_payment_statuses():
    """
    Fetch distinct payment statuses from the Payment table.
    """
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT DISTINCT payment_status FROM Payment")
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error fetching payment statuses: {e}")
        return []
    finally:
        connection.close()
