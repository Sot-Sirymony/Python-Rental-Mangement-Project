
import sqlite3
import pandas as pd

DATABASE = "rental_management_v2.db"

def fetch_room_summary():
    """Fetch room details for the summary report."""
    try:
        conn = sqlite3.connect(DATABASE)
        query = """
        SELECT id AS room_id, name, type, size, rental_price, occupancy_status
        FROM Room
        """
        df = pd.read_sql_query(query, conn)
    except sqlite3.Error as error:
        print("Error fetching room summary:", error)
        df = pd.DataFrame()  # Return an empty DataFrame on error
    finally:
        conn.close()
    return df


def fetch_financial_performance():
    """Fetch financial data for each room."""
    try:
        conn = sqlite3.connect(DATABASE)
        query = """
        SELECT r.id AS room_id, r.name, r.type, r.rental_price,
               SUM(p.amount) as total_income, 
               r.rental_price * COUNT(p.id) - SUM(p.amount) as outstanding
        FROM Room r
        LEFT JOIN Payment p ON r.id = p.room_id
        GROUP BY r.id
        """
        df = pd.read_sql_query(query, conn)
    except sqlite3.Error as error:
        print("Error fetching financial performance:", error)
        df = pd.DataFrame()  # Return an empty DataFrame on error
    finally:
        conn.close()
    return df



def fetch_occupancy_analysis():
    """Fetch room occupancy data for analysis."""
    try:
        conn = sqlite3.connect(DATABASE)
        query = """
        SELECT occupancy_status, COUNT(*) as count
        FROM Room
        GROUP BY occupancy_status
        """
        df = pd.read_sql_query(query, conn)
    except sqlite3.Error as error:
        print("Error fetching room occupancy analysis:", error)
        df = pd.DataFrame()  # Return an empty DataFrame on error
    finally:
        conn.close()
    return df


