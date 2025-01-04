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

def fetch_payments():
    """Fetch all payments."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM PaymentView;")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching payments: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def create_payment(tenant_id, room_id, amount, date, due_date, method, reference, notes):
    """Create a new payment."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT create_payment(%s, %s, %s, %s, %s, %s, %s, %s);",
                       (tenant_id, room_id, amount, date, due_date, method, reference, notes))
        connection.commit()
    except Exception as e:
        print(f"Error creating payment: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def update_payment(payment_id, amount, date, due_date, method, reference, notes, status):
    """Update payment details."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT update_payment(%s, %s, %s, %s, %s, %s, %s, %s);",
                       (payment_id, amount, date, due_date, method, reference, notes, status))
        connection.commit()
    except Exception as e:
        print(f"Error updating payment: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def delete_payment(payment_id):
    """Delete a payment."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT delete_payment(%s);", (payment_id,))
        connection.commit()
    except Exception as e:
        print(f"Error deleting payment: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def fetch_payment_data():
    """Fetch detailed payment data for Payment Report."""
    connection = get_connection()
    try:
        query = "SELECT * FROM PaymentReportView;"
        df = pd.read_sql_query(query, connection)
        return df
    except Exception as e:
        print(f"Error fetching payment data for report: {e}")
        return pd.DataFrame()
    finally:
        connection.close()
