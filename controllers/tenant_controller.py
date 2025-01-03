# import sqlite3

# def fetch_tenants():
#     connection = sqlite3.connect('rental_management_v2.db')
#     cursor = connection.cursor()
#     try:
#         cursor.execute("""
#         SELECT id, first_name || ' ' || last_name AS name, phone, email
#         FROM Tenant
#         """)
#         return cursor.fetchall()
#     except Exception as e:
#         print(f"Error fetching tenants: {e}")
#         return []
#     finally:
#         connection.close()     

# def add_tenant(first_name, last_name, phone, email):
#     connection = sqlite3.connect('rental_management_v2.db')
#     cursor = connection.cursor()
#     try:
#         cursor.execute("""
#         INSERT INTO Tenant (first_name, last_name, phone, email)
#         VALUES (?, ?, ?, ?)
#         """, (first_name, last_name, phone, email))
#         connection.commit()
#     except sqlite3.IntegrityError as e:
#         print(f"Integrity Error: {e}")
#         raise
#     except Exception as e:
#         print(f"Error adding tenant: {e}")
#         raise
#     finally:
#         connection.close()

# def update_tenant(tenant_id, first_name, last_name, phone, email):
#     connection = sqlite3.connect('rental_management_v2.db')
#     cursor = connection.cursor()
#     try:
#         cursor.execute("""
#         UPDATE Tenant
#         SET first_name = ?, last_name = ?, phone = ?, email = ?
#         WHERE id = ?
#         """, (first_name, last_name, phone, email, tenant_id))
#         connection.commit()
#     except Exception as e:
#         print(f"Error updating tenant: {e}")
#         raise
#     finally:
#         connection.close()      

# def fetch_rental_history(tenant_id):
#     import sqlite3
#     connection = sqlite3.connect('rental_management_v2.db')
#     cursor = connection.cursor()
#     try:
#         cursor.execute("""
#         SELECT r.name AS room_name, l.start_date, l.end_date, 
#                p.amount, p.date AS payment_date, p.method AS payment_method
#         FROM Lease l
#         JOIN Room r ON l.room_id = r.id
#         LEFT JOIN Payment p ON l.room_id = p.room_id AND l.tenant_id = p.tenant_id
#         WHERE l.tenant_id = ?
#         ORDER BY l.start_date DESC
#         """, (tenant_id,))
#         return cursor.fetchall()
#     except Exception as e:
#         print(f"Error fetching rental history: {e}")
#         return []
#     finally:
#         connection.close()



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

def delete_tenant(tenant_id):
    connection = sqlite3.connect('rental_management_v2.db')
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



