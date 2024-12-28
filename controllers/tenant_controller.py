import sqlite3

def fetch_tenants():
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        SELECT id, first_name || ' ' || last_name AS name, phone, email
        FROM Tenant
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching tenants: {e}")
        return []
    finally:
        connection.close()     

def add_tenant(first_name, last_name, phone, email):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        INSERT INTO Tenant (first_name, last_name, phone, email)
        VALUES (?, ?, ?, ?)
        """, (first_name, last_name, phone, email))
        connection.commit()
    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e}")
        raise
    except Exception as e:
        print(f"Error adding tenant: {e}")
        raise
    finally:
        connection.close()

def update_tenant(tenant_id, first_name, last_name, phone, email):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        UPDATE Tenant
        SET first_name = ?, last_name = ?, phone = ?, email = ?
        WHERE id = ?
        """, (first_name, last_name, phone, email, tenant_id))
        connection.commit()
    except Exception as e:
        print(f"Error updating tenant: {e}")
        raise
    finally:
        connection.close()      

def fetch_rental_history(tenant_id):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        SELECT Room.name, Lease.start_date, Lease.end_date, Payment.amount, Payment.date, Payment.method
        FROM Lease
        JOIN Room ON Lease.room_id = Room.id
        JOIN Payment ON Payment.tenant_id = Lease.tenant_id
        WHERE Lease.tenant_id = ?
        """, (tenant_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching rental history: {e}")
        return []
    finally:
        connection.close()

