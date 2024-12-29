import sqlite3

def add_payment(tenant, room, amount, date, method, reference=None):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        # Convert tenant to string to check if it's numeric
        tenant_str = str(tenant)

        # Determine if tenant is provided as ID or full name
        if tenant_str.isdigit():  # If the tenant is numeric, treat it as an ID
            tenant_id = int(tenant_str)
            cursor.execute("SELECT id FROM Tenant WHERE id = ?", (tenant_id,))
            result = cursor.fetchone()
            if not result:
                raise ValueError(f"Tenant with ID '{tenant_id}' not found in the database.")
        else:  # Otherwise, treat it as a full name
            cursor.execute("""
            SELECT id FROM Tenant WHERE first_name || ' ' || last_name = ?
            """, (tenant_str,))
            result = cursor.fetchone()
            if not result:
                raise ValueError(f"Tenant '{tenant}' not found in the database.")
            tenant_id = result[0]

        # Convert room to string to check if it's numeric
        room_str = str(room)

        # Determine if room is provided as ID or name
        if room_str.isdigit():  # If the room is numeric, treat it as an ID
            room_id = int(room_str)
            cursor.execute("SELECT id FROM Room WHERE id = ?", (room_id,))
            result = cursor.fetchone()
            if not result:
                raise ValueError(f"Room with ID '{room_id}' not found in the database.")
        else:  # Otherwise, treat it as a name
            cursor.execute("SELECT id FROM Room WHERE name = ?", (room_str,))
            result = cursor.fetchone()
            if not result:
                raise ValueError(f"Room '{room}' not found in the database.")
            room_id = result[0]

        # Insert payment
        cursor.execute("""
        INSERT INTO Payment (tenant_id, room_id, amount, date, method, reference)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (tenant_id, room_id, amount, date, method, reference))
        connection.commit()
        print("Payment added successfully!")
    except Exception as e:
        print(f"Error adding payment: {e}")
        raise
    finally:
        connection.close()


def get_all_payments():
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT 
        (SELECT first_name || ' ' || last_name FROM Tenant WHERE id = p.tenant_id) AS tenant,
        (SELECT name FROM Room WHERE id = p.room_id) AS room,
        p.amount, p.date, p.method 
    FROM Payment p
    """)
    payments = [{"tenant": row[0], "room": row[1], "amount": row[2], "date": row[3], "method": row[4]} for row in cursor.fetchall()]
    connection.close()
    return payments
# 1. Record a payment
def record_payment(tenant_id, room_id, amount, payment_method, payment_date, payment_reference):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        INSERT INTO Payment (tenant_id, room_id, amount, method, payment_date, reference)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (tenant_id, room_id, amount, payment_method, payment_date, payment_reference))
        connection.commit()
    except Exception as e:
        print(f"Error recording payment: {e}")
        raise
    finally:
        connection.close()


def fetch_payment_history(tenant_id=None, room_id=None, method=None, start_date=None, end_date=None):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        query = """
        SELECT p.id, t.first_name || ' ' || t.last_name AS tenant_name, r.name AS room_name, 
               p.amount, p.method, p.date, p.reference
        FROM Payment p
        JOIN Tenant t ON p.tenant_id = t.id
        JOIN Room r ON p.room_id = r.id
        WHERE 1=1
        """
        params = []
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
        
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching payment history: {e}")
        return []
    finally:
        connection.close()


# 3. Generate an invoice
def generate_invoice(tenant_id, room_id, rental_period, amount_due, due_date, custom_notes=""):
    # Placeholder for invoice generation logic.
    # This can save the invoice to a database or generate a PDF.
    return {
        "tenant_id": tenant_id,
        "room_id": room_id,
        "rental_period": rental_period,
        "amount_due": amount_due,
        "due_date": due_date,
        "custom_notes": custom_notes
    }

# 4. Generate a receipt
def generate_receipt(payment_id):
    # Placeholder for receipt generation logic.
    # This can save the receipt to a database or generate a PDF.
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        SELECT p.id, t.first_name || ' ' || t.last_name AS tenant_name, r.name AS room_name, 
               p.amount, p.method, p.payment_date, p.reference
        FROM Payment p
        JOIN Tenant t ON p.tenant_id = t.id
        JOIN Room r ON p.room_id = r.id
        WHERE p.id = ?
        """, (payment_id,))
        receipt_data = cursor.fetchone()
        return receipt_data
    except Exception as e:
        print(f"Error generating receipt: {e}")
        return None
    finally:
        connection.close()
        
def delete_payment(payment_id):
    """
    Delete a payment record by its ID.
    """
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Payment WHERE id = ?", (payment_id,))
        connection.commit()
    except Exception as e:
        print(f"Error deleting payment: {e}")
        raise
    finally:
        connection.close()        