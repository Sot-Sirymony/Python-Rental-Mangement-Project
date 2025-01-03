

import sqlite3
import pandas as pd
DATABASE = "rental_management_v2.db"

def fetch_tenants():
    connection = sqlite3.connect(DATABASE)
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
    connection = sqlite3.connect(DATABASE)
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
    connection = sqlite3.connect(DATABASE)
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

def delete_tenant(tenant_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    try:
        # Delete the tenant
        cursor.execute("""
        DELETE FROM Tenant
        WHERE id = ?
        """, (tenant_id,))
        connection.commit()
    except Exception as e:
        print(f"Error deleting tenant: {e}")
        raise
    finally:
        connection.close()
#for report

def fetch_tenant_data():
    """Fetch detailed tenant data for Payment Report."""
    connection = sqlite3.connect(DATABASE)
    try:
        query = """
        SELECT 
            t.id AS tenant_id,
            t.first_name || ' ' || t.last_name AS tenant_name,
            t.phone AS contact_number,
            t.email AS email_address,
            (SELECT COUNT(*) FROM Lease WHERE Lease.tenant_id = t.id AND status = 'Active') AS active_leases,
            (SELECT SUM(amount) FROM Payment WHERE Payment.tenant_id = t.id AND payment_status = 'Overdue') AS overdue_balance
        FROM Tenant t
        """
        df = pd.read_sql_query(query, connection)
        return df
    except Exception as e:
        print(f"Error fetching tenant data for report: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    finally:
        connection.close()


