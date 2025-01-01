
from sqlite3 import connect

def set_rental_price_and_terms(room_id, rental_price, payment_frequency, security_deposit, grace_period):
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        UPDATE Room
        SET rental_price = ?,
            payment_frequency = ?,
            security_deposit = ?,
            grace_period = ?
        WHERE id = ?
        """, (rental_price, payment_frequency, security_deposit, grace_period, room_id))
        connection.commit()
    except Exception as e:
        print(f"Error setting rental terms: {e}")
    finally:
        connection.close()

def update_tenant_for_room(room_id, tenant_id):
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        UPDATE Room
        SET tenant_id = ?
        WHERE id = ?
        """, (tenant_id, room_id))
        connection.commit()
    except Exception as e:
        print(f"Error updating tenant for room: {e}")
        raise
    finally:
        connection.close()

def update_occupancy_status(room_id, status):
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        UPDATE Room
        SET occupancy_status = ?
        WHERE id = ?
        """, (status, room_id))
        connection.commit()
    except Exception as e:
        print(f"Error updating occupancy status: {e}")
    finally:
        connection.close()
def fetch_room_details_with_related_data():
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        query = """
        SELECT
            r.id AS room_id,                               -- Room ID
            r.name AS room_name,                           -- Room Name
            r.type AS room_type,                           -- Room Type
            r.rental_price,                                -- Rental Price
            r.payment_frequency,                          -- Payment Frequency
            r.security_deposit,                           -- Security Deposit
            r.grace_period,                               -- Grace Period
            r.occupancy_status,                           -- Current Occupancy Status
            COALESCE(t.first_name || ' ' || t.last_name, 'No Tenant') AS tenant_name, -- Tenant Name or 'No Tenant'
            COALESCE(b.status, r.occupancy_status) AS dynamic_status, -- Dynamic status based on booking
            COALESCE(SUM(p.amount), 0) AS total_payments, -- Total Payment Amount
            MAX(p.date) AS last_payment_date,             -- Last Payment Date
            MAX(p.due_date) AS latest_due_date,           -- Latest Due Date
            GROUP_CONCAT(p.reference_number) AS payment_references, -- All Payment References for the Room
            MAX(l.start_date) AS lease_start_date,        -- Lease Start Date
            MAX(l.end_date) AS lease_end_date             -- Lease End Date
        FROM Room r
        LEFT JOIN Tenant t ON r.tenant_id = t.id          -- Join with Tenant Table
        LEFT JOIN (
            SELECT room_id, status
            FROM Booking
            WHERE status IN ('Pending', 'Active')         -- Filter relevant booking statuses
        ) b ON r.id = b.room_id                           -- Join with Booking Table
        LEFT JOIN Payment p ON r.id = p.room_id           -- Join with Payment Table
        LEFT JOIN Lease l ON r.id = l.room_id AND l.status = 'Active' -- Join with Lease Table (Active Leases)
        GROUP BY 
            r.id, r.name, r.type, r.rental_price, 
            r.payment_frequency, r.security_deposit, 
            r.grace_period, r.occupancy_status,
            t.first_name, t.last_name, b.status           -- Ensure all selected columns are grouped
        ORDER BY r.id;                                    -- Sort results by Room ID
        """
        
        cursor.execute(query)
        result = cursor.fetchall()
        print(f"Fetched {len(result)} room records with related data.")
        return result

    except Exception as e:
        print(f"Error fetching room details with related data: {e}")
        return []

    finally:
        connection.close()



def create_lease(room_id, tenant_id, start_date, end_date):
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        # Insert the lease
        cursor.execute("""
        INSERT INTO Lease (room_id, tenant_id, start_date, end_date)
        VALUES (?, ?, ?, ?)
        """, (room_id, tenant_id, start_date, end_date))

        # Update the room's occupancy status
        cursor.execute("""
        UPDATE Room
        SET occupancy_status = 'Rented', tenant_id = ?
        WHERE id = ?
        """, (tenant_id, room_id))

        connection.commit()
    except Exception as e:
        print(f"Error creating lease: {e}")
        raise
    finally:
        connection.close()

def fetch_leases(room_id=None, tenant_id=None):
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        query = """
        SELECT l.id, r.name AS room_name, t.first_name || ' ' || t.last_name AS tenant_name,
               l.start_date, l.end_date, l.status
        FROM Lease l
        JOIN Room r ON l.room_id = r.id
        JOIN Tenant t ON l.tenant_id = t.id
        WHERE 1=1
        """
        params = []
        if room_id:
            query += " AND l.room_id = ?"
            params.append(room_id)
        if tenant_id:
            query += " AND l.tenant_id = ?"
            params.append(tenant_id)

        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching leases: {e}")
        return []
    finally:
        connection.close()

def update_lease(lease_id, start_date, end_date, status):
    connection = connect('rental_management_v2.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        UPDATE Lease
        SET start_date = ?, end_date = ?, status = ?
        WHERE id = ?
        """, (start_date, end_date, status, lease_id))
        connection.commit()
    except Exception as e:
        print(f"Error updating lease: {e}")
        raise
    finally:
        connection.close()

       
        
        
     
