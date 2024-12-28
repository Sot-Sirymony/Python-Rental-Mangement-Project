import sqlite3

def initialize_db():
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()

    # Create Property table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Property (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        address TEXT,
        description TEXT,
        amenities TEXT
    );
    """)

    # Create Room table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Room (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id INTEGER NOT NULL,
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
        FOREIGN KEY (property_id) REFERENCES Property (id) ON DELETE CASCADE
    );
    """)

    # Create Tenant table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Tenant (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        phone TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """)

    # Create Payment table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Payment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id INTEGER NOT NULL,
        room_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        method TEXT,
        FOREIGN KEY (tenant_id) REFERENCES Tenant (id),
        FOREIGN KEY (room_id) REFERENCES Room (id)
    );
    """)

    # Create Lease table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Lease (
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
    CREATE TABLE IF NOT EXISTS Booking (
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
    initialize_db()
