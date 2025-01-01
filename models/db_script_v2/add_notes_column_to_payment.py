import sqlite3

def add_notes_column_to_payment():
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        # Check if the column already exists
        cursor.execute("PRAGMA table_info(Payment)")
        columns = [info[1] for info in cursor.fetchall()]
        if "notes" in columns:
            print("The 'notes' column already exists in the Payment table.")
            return

        # Add the notes column
        cursor.execute("ALTER TABLE Payment ADD COLUMN notes TEXT")
        connection.commit()
        print("The 'notes' column has been successfully added to the Payment table.")
    except Exception as e:
        print(f"Error adding 'notes' column to the Payment table: {e}")
    finally:
        connection.close()

# Call the function
add_notes_column_to_payment()
