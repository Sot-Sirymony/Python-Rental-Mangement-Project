import psycopg2
import pandas as pd

DATABASE = {
    'dbname': 'rental_management_db',
    'user': 'postgres',
    'password': 'Mony@1144',
    'host': 'localhost',
    'port': 5432
}

# def get_connection():
#     return psycopg2.connect(**DATABASE)
def get_connection():
    try:
        connection = psycopg2.connect(**DATABASE)
        print("Connection successful!")
        return connection  # Return the open connection
    except Exception as e:
        print(f"Connection failed: {e}")
        return None  # Return None if the connection fails

def fetch_room_summary():
    """Fetch room details for the summary report."""
    connection = get_connection()
    try:
        query = "SELECT * FROM RoomSummaryView;"
        df = pd.read_sql_query(query, connection)
    except Exception as error:
        print("Error fetching room summary:", error)
        df = pd.DataFrame()  # Return an empty DataFrame on error
    finally:
        connection.close()
    return df

def fetch_financial_performance():
    """Fetch financial data for each room."""
    connection = get_connection()
    try:
        query = "SELECT * FROM RoomFinancialPerformanceView;"
        df = pd.read_sql_query(query, connection)
    except Exception as error:
        print("Error fetching financial performance:", error)
        df = pd.DataFrame()  # Return an empty DataFrame on error
    finally:
        connection.close()
    return df

def fetch_occupancy_analysis():
    """Fetch room occupancy data for analysis."""
    connection = get_connection()
    try:
        query = "SELECT * FROM RoomOccupancyAnalysisView;"
        df = pd.read_sql_query(query, connection)
    except Exception as error:
        print("Error fetching room occupancy analysis:", error)
        df = pd.DataFrame()  # Return an empty DataFrame on error
    finally:
        connection.close()
    return df
