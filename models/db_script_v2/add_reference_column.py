import sqlite3

def add_reference_column():
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("ALTER TABLE Payment ADD COLUMN reference TEXT")
        connection.commit()
        print("Column 'reference' added successfully.")
    except Exception as e:
        print(f"Error adding column 'reference': {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    add_reference_column()
