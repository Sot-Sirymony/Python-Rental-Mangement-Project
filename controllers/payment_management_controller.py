import sqlite3
import pandas as pd

DATABASE = "rental_management_v2.db"

def fetch_payments():
    """Fetch all payments."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        cursor.execute("""
        SELECT p.id, r.name AS room_name, t.first_name || ' ' || t.last_name AS tenant_name,
               p.amount, p.date, p.due_date, p.method, p.payment_status, p.reference_number, p.notes
        FROM Payment p
        JOIN Room r ON p.room_id = r.id
        JOIN Tenant t ON p.tenant_id = t.id
        ORDER BY p.date DESC
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching payments: {e}")
        return []
    finally:
        connection.close()

def create_payment(tenant_id, room_id, amount, date, due_date, method, reference, notes):
    """Create a new payment."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        cursor.execute("""
        INSERT INTO Payment (tenant_id, room_id, amount, date, due_date, method, reference_number, notes, payment_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Paid')
        """, (tenant_id, room_id, amount, date, due_date, method, reference, notes))
        cursor.execute("""
        UPDATE Room
        SET total_rent_collected = total_rent_collected + ?
        WHERE id = ?
        """, (amount, room_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error creating payment: {e}")
        raise
    finally:
        connection.close()

def update_payment(payment_id, amount, date, due_date, method, reference, notes, status):
    """Update payment details."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        # Fetch the original payment amount
        cursor.execute("SELECT room_id, amount FROM Payment WHERE id = ?", (payment_id,))
        room_id, original_amount = cursor.fetchone()

        # Update payment details
        cursor.execute("""
        UPDATE Payment
        SET amount = ?, date = ?, due_date = ?, method = ?, reference_number = ?, notes = ?, payment_status = ?
        WHERE id = ?
        """, (amount, date, due_date, method, reference, notes, status, payment_id))

        # Adjust room's total rent collected
        cursor.execute("""
        UPDATE Room
        SET total_rent_collected = total_rent_collected - ? + ?
        WHERE id = ?
        """, (original_amount, amount, room_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error updating payment: {e}")
        raise
    finally:
        connection.close()

def delete_payment(payment_id):
    """Delete a payment."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        # Fetch the original payment amount
        cursor.execute("SELECT room_id, amount FROM Payment WHERE id = ?", (payment_id,))
        room_id, amount = cursor.fetchone()

        # Delete the payment
        cursor.execute("DELETE FROM Payment WHERE id = ?", (payment_id,))

        # Adjust room's total rent collected
        cursor.execute("""
        UPDATE Room
        SET total_rent_collected = total_rent_collected - ?
        WHERE id = ?
        """, (amount, room_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error deleting payment: {e}")
        raise
    finally:
        connection.close()
        
        
def fetch_available_rooms():
    """Fetch all available rooms."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        cursor.execute("""
        SELECT id, name 
        FROM Room 
        WHERE occupancy_status = 'Available'
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
        SELECT id, first_name || ' ' || last_name AS name
        FROM Tenant
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching tenants: {e}")
        return []
    finally:
        connection.close()  
         
## for mapyemnt_report_controller        
def fetch_payment_data():
    """Fetch detailed payment data for Payment Report."""
    connection = sqlite3.connect(DATABASE)
    try:
        query = """
        SELECT 
            p.id AS payment_id,
            r.id AS room_id,
            r.name AS room_name,
            t.id AS tenant_id,
            t.first_name || ' ' || t.last_name AS tenant_name,
            p.amount AS amount_paid,
            p.due_date,
            p.date AS payment_date,
            p.payment_status AS status,
            (CASE 
                WHEN p.payment_status = 'Overdue' THEN p.amount 
                ELSE 0 
            END) AS overdue_amount
        FROM Payment p
        JOIN Room r ON p.room_id = r.id
        JOIN Tenant t ON p.tenant_id = t.id
        """
        df = pd.read_sql_query(query, connection)
        return df
    except Exception as e:
        print(f"Error fetching payment data for report: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    finally:
        connection.close()             
