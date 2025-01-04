import psycopg2
import pandas as pd

DATABASE = {
    'dbname': 'your_db_name',
    'user': 'your_user',
    'password': 'your_password',
    'host': 'localhost',
    'port': 5432
}

def get_connection():
    return psycopg2.connect(**DATABASE)

def fetch_tenants():
    """Fetch all tenants."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM TenantView;")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching tenants: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def add_tenant(first_name, last_name, phone, email):
    """Add a new tenant."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT add_tenant(%s, %s, %s, %s);",
                       (first_name, last_name, phone, email))
        connection.commit()
    except Exception as e:
        print(f"Error adding tenant: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def update_tenant(tenant_id, first_name, last_name, phone, email):
    """Update an existing tenant."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT update_tenant(%s, %s, %s, %s, %s);",
                       (tenant_id, first_name, last_name, phone, email))
        connection.commit()
    except Exception as e:
        print(f"Error updating tenant: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def delete_tenant(tenant_id):
    """Delete a tenant."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT delete_tenant(%s);", (tenant_id,))
        connection.commit()
    except Exception as e:
        print(f"Error deleting tenant: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def fetch_tenant_data():
    """Fetch detailed tenant data for the report."""
    connection = get_connection()
    try:
        query = "SELECT * FROM TenantReportView;"
        df = pd.read_sql_query(query, connection)
        return df
    except Exception as e:
        print(f"Error fetching tenant data for report: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    finally:
        connection.close()
