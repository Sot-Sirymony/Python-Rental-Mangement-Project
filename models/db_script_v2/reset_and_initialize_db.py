
import sqlite3

def reset_and_initialize_db():
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()

    # Drop existing tables if they exist
    cursor.execute("DROP TABLE IF EXISTS Booking;")
    cursor.execute("DROP TABLE IF EXISTS Lease;")
    cursor.execute("DROP TABLE IF EXISTS Payment;")
    cursor.execute("DROP TABLE IF EXISTS Tenant;")
    cursor.execute("DROP TABLE IF EXISTS Room;")

    # Create Room table
    cursor.execute("""
    CREATE TABLE Room (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT,
        size REAL,
        rental_price REAL,
        payment_frequency TEXT,
        security_deposit REAL,
        grace_period INTEGER,
        occupancy_status TEXT DEFAULT 'Available',
        tenant_id INTEGER REFERENCES Tenant (id) ON DELETE SET NULL,
        amenities TEXT,
        total_rent_collected REAL DEFAULT 0
    );
    """)

    # Create Tenant table
    cursor.execute("""
    CREATE TABLE Tenant (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        phone TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """)

    # Create Payment table
    cursor.execute("""
    CREATE TABLE Payment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id INTEGER NOT NULL,
        room_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        method TEXT,
        due_date TEXT,
        notes TEXT,
        payment_status TEXT DEFAULT 'Pending',
        reference_number TEXT,
        FOREIGN KEY (tenant_id) REFERENCES Tenant (id),
        FOREIGN KEY (room_id) REFERENCES Room (id)
    );
    """)

    # Create Lease table
    cursor.execute("""
    CREATE TABLE Lease (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER NOT NULL,
        tenant_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        status TEXT DEFAULT 'Active',
        FOREIGN KEY (room_id) REFERENCES Room (id),
        FOREIGN KEY (tenant_id) REFERENCES Tenant (id)
    );
    """)

    # Create Booking table
    cursor.execute("""
    CREATE TABLE Booking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER NOT NULL,
        tenant_id INTEGER NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        notes TEXT,
        status TEXT DEFAULT 'Pending',  -- Pending, Active, Completed, Canceled
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (room_id) REFERENCES Room (id),
        FOREIGN KEY (tenant_id) REFERENCES Tenant (id)
    );
    """)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    reset_and_initialize_db()

