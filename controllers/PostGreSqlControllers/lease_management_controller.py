import psycopg2
import pandas as pd

DATABASE = {
    'dbname': 'rental_management_db',
    'user': 'postgres',
    'password': 'Mony@1144',
    'host': 'localhost',
    'port': 5432
}

def get_connection():
    try:
        connection = psycopg2.connect(**DATABASE)
        print("Connection successful!")
        return connection  # Return the open connection
    except Exception as e:
        print(f"Connection failed: {e}")
        return None  # Return None if the connection fails

def fetch_leases():
    """Fetch all leases."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM LeaseView;")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching leases: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def cancel_lease(lease_id):
    """Cancel a lease."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT cancel_lease(%s);", (lease_id,))
        connection.commit()
    except Exception as e:
        print(f"Error canceling lease: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def delete_lease(lease_id):
    """Delete a lease."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT delete_lease(%s);", (lease_id,))
        connection.commit()
    except Exception as e:
        print(f"Error deleting lease: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def create_lease(room_id, tenant_id, start_date, end_date):
    """Create a new lease."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT create_lease(%s, %s, %s, %s);",
                       (room_id, tenant_id, start_date, end_date))
        connection.commit()
    except Exception as e:
        print(f"Error creating lease: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def update_lease(lease_id, start_date, end_date, status):
    """Update lease details."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT update_lease(%s, %s, %s, %s);",
                       (lease_id, start_date, end_date, status))
        connection.commit()
    except Exception as e:
        print(f"Error updating lease: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def fetch_lease_data():
    """Fetch detailed lease data for the Lease Report."""
    connection = get_connection()
    try:
        query = "SELECT * FROM LeaseReportView;"
        df = pd.read_sql_query(query, connection)
        return df
    except Exception as e:
        print(f"Error fetching lease data for report: {e}")
        return pd.DataFrame()
    finally:
        connection.close()
