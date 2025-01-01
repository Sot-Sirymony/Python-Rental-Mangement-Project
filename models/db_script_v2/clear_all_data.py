import sqlite3

def clear_all_data():
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()

    try:
        # Disable foreign key constraints temporarily to avoid errors
        cursor.execute("PRAGMA foreign_keys=OFF;")
        
        # Clear data from all tables
        cursor.execute("DELETE FROM Payment;")
        cursor.execute("DELETE FROM Lease;")
        cursor.execute("DELETE FROM Booking;")
        cursor.execute("DELETE FROM Room;")
        cursor.execute("DELETE FROM Tenant;")
        cursor.execute("DELETE FROM Property;")
        
        # Re-enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys=ON;")
        
        connection.commit()
        print("All data cleared successfully.")
    except Exception as e:
        print(f"Error clearing data: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    clear_all_data()
