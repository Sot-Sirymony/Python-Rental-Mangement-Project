--Create Room table
CREATE TABLE Room (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
type TEXT,
size NUMERIC, -- PostgreSQL uses NUMERIC for precise real numbers
rental_price NUMERIC,
payment_frequency TEXT,
security_deposit NUMERIC,
grace_period INTEGER,
occupancy_status TEXT DEFAULT 'Available',
tenant_id INTEGER REFERENCES Tenant (id) ON DELETE SET NULL,
amenities TEXT,
total_rent_collected NUMERIC DEFAULT 0
);
--Create Tenant table
CREATE TABLE Tenant (
id SERIAL PRIMARY KEY,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
phone TEXT UNIQUE NOT NULL,
email TEXT UNIQUE NOT NULL
);
--Create Payment table
CREATE TABLE Payment (
id SERIAL PRIMARY KEY,
tenant_id INTEGER NOT NULL REFERENCES Tenant (id),
room_id INTEGER NOT NULL REFERENCES Room (id),
amount NUMERIC NOT NULL,
date DATE NOT NULL,
method TEXT,
due_date DATE,
notes TEXT,
payment_status TEXT DEFAULT 'Pending',
reference_number TEXT
);
--Create Lease table
CREATE TABLE Lease (
id SERIAL PRIMARY KEY,
room_id INTEGER NOT NULL REFERENCES Room (id),
tenant_id INTEGER NOT NULL REFERENCES Tenant (id),
start_date DATE NOT NULL,
end_date DATE NOT NULL,
status TEXT DEFAULT 'Active'
);
--Create Booking table
CREATE TABLE Booking (
id SERIAL PRIMARY KEY,
room_id INTEGER NOT NULL REFERENCES Room (id),
tenant_id INTEGER NOT NULL REFERENCES Tenant (id),
start_date DATE NOT NULL,
end_date DATE NOT NULL,
notes TEXT,
status TEXT DEFAULT 'Pending', -- Pending, Active, Completed, Canceled
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- room managment
   --fetch_room_details_with_booking
   CREATE VIEW RoomDetailsWithBooking AS
    SELECT
        r.id,
        r.name,
        r.type,
        r.rental_price,
        r.payment_frequency,
        r.security_deposit,
        r.grace_period,
        r.occupancy_status,
        t.first_name || ' ' || t.last_name AS tenant_name,
        COALESCE(b.status, r.occupancy_status) AS dynamic_status
    FROM Room r
    LEFT JOIN Tenant t ON r.tenant_id = t.id
    LEFT JOIN (
        SELECT room_id, status
        FROM Booking
        WHERE status IN ('Pending', 'Active')
    ) b ON r.id = b.room_id;
    -- fetch_room_data
    CREATE VIEW RoomDataReport AS
    SELECT
        r.id AS room_id,
        r.name AS room_name,
        r.type AS room_type,
        r.rental_price,
        r.occupancy_status,
        r.size AS room_size,
        r.amenities,
        (SELECT COALESCE(SUM(p.amount), 0)
        FROM Payment p
        WHERE p.room_id = r.id) AS total_rent_collected,
        (SELECT COUNT(*)
        FROM Lease l
        WHERE l.room_id = r.id AND l.status = 'Active') AS active_lease_count,
        (SELECT COUNT(*)
        FROM Payment p
        WHERE p.room_id = r.id AND p.payment_status = 'Overdue') AS overdue_payments
    FROM Room r;
    -- add room
    CREATE OR REPLACE FUNCTION add_room(
    room_name TEXT,
    room_type TEXT,
    room_size NUMERIC,
    rental_price NUMERIC,
    room_amenities TEXT
    )
    RETURNS VOID AS $$
    BEGIN
        INSERT INTO Room (name, type, size, rental_price, amenities)
        VALUES (room_name, room_type, room_size, rental_price, room_amenities);
    END;
    $$ LANGUAGE plpgsql;
    -- update_room
    CREATE OR REPLACE FUNCTION update_room(
    room_id INT,
    room_name TEXT,
    room_type TEXT,
    room_size NUMERIC,
    rental_price NUMERIC,
    room_amenities TEXT,
    occupancy_status TEXT
    )
    RETURNS VOID AS $$
    BEGIN
        UPDATE Room
        SET name = room_name,
            type = room_type,
            size = room_size,
            rental_price = rental_price,
            amenities = room_amenities,
            occupancy_status = occupancy_status
        WHERE id = room_id;
    END;
    $$ LANGUAGE plpgsql;
    --delete_room
    CREATE OR REPLACE FUNCTION delete_room(room_id INT)
    RETURNS VOID AS $$
    BEGIN
        DELETE FROM Room WHERE id = room_id;
    END;
    $$ LANGUAGE plpgsql;
    -- Fetch Available Rooms
    CREATE VIEW AvailableRooms AS
    SELECT id, name
    FROM Room
    WHERE occupancy_status = 'Available';

-- tenant management        
    -- fetch_tenants
    CREATE VIEW TenantView AS
    SELECT
        id,
        first_name || ' ' || last_name AS name,
        phone,
        email
    FROM Tenant;
    -- fetch_tenant_data
    CREATE VIEW TenantReportView AS
    SELECT
        t.id AS tenant_id,
        t.first_name || ' ' || t.last_name AS tenant_name,
        t.phone AS contact_number,
        t.email AS email_address,
        (SELECT COUNT(*) FROM Lease WHERE Lease.tenant_id = t.id AND status = 'Active') AS active_leases,
        (SELECT COALESCE(SUM(amount), 0) FROM Payment WHERE Payment.tenant_id = t.id AND payment_status = 'Overdue') AS overdue_balance
    FROM Tenant t;
    -- update_tenant
    CREATE OR REPLACE FUNCTION update_tenant(
    tenant_id INT,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    email TEXT
    )
    RETURNS VOID AS $$
    BEGIN
        UPDATE Tenant
        SET first_name = first_name,
            last_name = last_name,
            phone = phone,
            email = email
        WHERE id = tenant_id;
    END;
    $$ LANGUAGE plpgsql;
    -- delete_tenant
    CREATE OR REPLACE FUNCTION delete_tenant(tenant_id INT)
    RETURNS VOID AS $$
    BEGIN
        DELETE FROM Tenant WHERE id = tenant_id;
    END;
    $$ LANGUAGE plpgsql;


-- lease management
    --fetch_leases
    CREATE VIEW LeaseView AS
    SELECT
        l.id AS lease_id,
        r.name AS room_name,
        t.first_name || ' ' || t.last_name AS tenant_name,
        l.start_date,
        l.end_date,
        l.status
    FROM Lease l
    JOIN Room r ON l.room_id = r.id
    JOIN Tenant t ON l.tenant_id = t.id
    ORDER BY l.start_date DESC;
    -- fetch_lease_data
    CREATE VIEW LeaseReportView AS
    SELECT
        l.id AS lease_id,
        r.id AS room_id,
        r.name AS room_name,
        t.first_name || ' ' || t.last_name AS tenant_name,
        t.id AS tenant_id,
        l.start_date,
        l.end_date,
        l.status,
        (l.end_date::DATE - l.start_date::DATE) AS lease_duration,
        CASE
            WHEN l.status = 'Active' THEN 1
            ELSE 0
        END AS active_lease_flag
    FROM Lease l
    JOIN Room r ON l.room_id = r.id
    JOIN Tenant t ON l.tenant_id = t.id;
-- payment management
    -- fetch_payments
    CREATE VIEW PaymentView AS
    SELECT
        p.id,
        r.name AS room_name,
        t.first_name || ' ' || t.last_name AS tenant_name,
        p.amount,
        p.date,
        p.due_date,
        p.method,
        p.payment_status,
        p.reference_number,
        p.notes
    FROM Payment p
    JOIN Room r ON p.room_id = r.id
    JOIN Tenant t ON p.tenant_id = t.id
    ORDER BY p.date DESC;
    --fetch_payment_data
    CREATE VIEW PaymentReportView AS
    SELECT
        p.id AS payment_id,
        r.id AS room_id,
        r.name AS room_name,
        t.id AS tenant_id,
        t.first_name || ' ' || t.last_name AS tenant_name,
        p.amount AS amount_paid,
        p.due_date,
        p.date AS payment_date,
        p.payment_status AS status,
        CASE
            WHEN p.payment_status = 'Overdue' THEN p.amount
            ELSE 0
        END AS overdue_amount
    FROM Payment p
    JOIN Room r ON p.room_id = r.id
    JOIN Tenant t ON p.tenant_id = t.id;
    -- create_payment
    CREATE OR REPLACE FUNCTION create_payment(
    tenant_id INT,
    room_id INT,
    amount NUMERIC,
    payment_date DATE,
    due_date DATE,
    method TEXT,
    reference TEXT,
    notes TEXT
    )
    RETURNS VOID AS $$
    BEGIN
        INSERT INTO Payment (tenant_id, room_id, amount, date, due_date, method, reference_number, notes, payment_status)
        VALUES (tenant_id, room_id, amount, payment_date, due_date, method, reference, notes, 'Paid');

        UPDATE Room
        SET total_rent_collected = total_rent_collected + amount
        WHERE id = room_id;
    END;
    $$ LANGUAGE plpgsql;
    -- update_payment
    CREATE OR REPLACE FUNCTION update_payment(
    payment_id INT,
    amount NUMERIC,
    payment_date DATE,
    due_date DATE,
    method TEXT,
    reference TEXT,
    notes TEXT,
    status TEXT
    )
    RETURNS VOID AS $$
    DECLARE
        room_id INT;
        original_amount NUMERIC;
    BEGIN
        -- Fetch original payment amount and room_id
        SELECT room_id, amount INTO room_id, original_amount
        FROM Payment WHERE id = payment_id;

        -- Update payment details
        UPDATE Payment
        SET amount = amount,
            date = payment_date,
            due_date = due_date,
            method = method,
            reference_number = reference,
            notes = notes,
            payment_status = status
        WHERE id = payment_id;

        -- Adjust room's total rent collected
        UPDATE Room
        SET total_rent_collected = total_rent_collected - original_amount + amount
        WHERE id = room_id;
    END;
    $$ LANGUAGE plpgsql;
    --delete_payment
    CREATE OR REPLACE FUNCTION delete_payment(payment_id INT)
    RETURNS VOID AS $$
    DECLARE
        room_id INT;
        amount NUMERIC;
    BEGIN
        -- Fetch original payment amount and room_id
        SELECT room_id, amount INTO room_id, amount
        FROM Payment WHERE id = payment_id;

        -- Delete the payment
        DELETE FROM Payment WHERE id = payment_id;

        -- Adjust room's total rent collected
        UPDATE Room
        SET total_rent_collected = total_rent_collected - amount
        WHERE id = room_id;
    END;
    $$ LANGUAGE plpgsql;


-- report
  -- room report
    -- fetch_room_summary
    CREATE VIEW RoomSummaryView AS
    SELECT
        id AS room_id,
        name,
        type,
        size,
        rental_price,
        occupancy_status
    FROM Room;
    -- fetch_financial_performance
    CREATE VIEW RoomFinancialPerformanceView AS
    SELECT
        r.id AS room_id,
        r.name,
        r.type,
        r.rental_price,
        COALESCE(SUM(p.amount), 0) AS total_income,
        r.rental_price * COUNT(p.id) - COALESCE(SUM(p.amount), 0) AS outstanding
    FROM Room r
    LEFT JOIN Payment p ON r.id = p.room_id
    GROUP BY r.id, r.name, r.type, r.rental_price;

    -- fetch_occupancy_analysis
    CREATE VIEW RoomOccupancyAnalysisView AS
    SELECT
        occupancy_status,
        COUNT(*) AS count
    FROM Room
    GROUP BY occupancy_status;
