-- public.tenant definition

-- Drop table

-- DROP TABLE public.tenant;

CREATE TABLE public.tenant (
	id serial4 NOT NULL,
	first_name text NOT NULL,
	last_name text NOT NULL,
	phone text NOT NULL,
	email text NOT NULL,
	CONSTRAINT tenant_email_key UNIQUE (email),
	CONSTRAINT tenant_phone_key UNIQUE (phone),
	CONSTRAINT tenant_pkey PRIMARY KEY (id)
);

-- public.room definition

-- Drop table

-- DROP TABLE public.room;

CREATE TABLE public.room (
	id serial4 NOT NULL,
	"name" text NOT NULL,
	"type" text NULL,
	"size" numeric NULL,
	rental_price numeric NULL,
	payment_frequency text NULL,
	security_deposit numeric NULL,
	grace_period int4 NULL,
	occupancy_status text DEFAULT 'Available'::text NULL,
	tenant_id int4 NULL,
	amenities text NULL,
	total_rent_collected numeric DEFAULT 0 NULL,
	CONSTRAINT room_pkey PRIMARY KEY (id)
);


-- public.room foreign keys

ALTER TABLE public.room ADD CONSTRAINT room_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenant(id) ON DELETE SET NULL;


-- public.payment definition

-- Drop table

-- DROP TABLE public.payment;

CREATE TABLE public.payment (
	id serial4 NOT NULL,
	tenant_id int4 NOT NULL,
	room_id int4 NOT NULL,
	amount numeric NOT NULL,
	"date" date NOT NULL,
	"method" text NULL,
	due_date date NULL,
	notes text NULL,
	payment_status text DEFAULT 'Pending'::text NULL,
	reference_number text NULL,
	CONSTRAINT payment_pkey PRIMARY KEY (id)
);


-- public.payment foreign keys

ALTER TABLE public.payment ADD CONSTRAINT payment_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.room(id);
ALTER TABLE public.payment ADD CONSTRAINT payment_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenant(id);


-- public.lease definition

-- Drop table

-- DROP TABLE public.lease;

CREATE TABLE public.lease (
	id serial4 NOT NULL,
	room_id int4 NOT NULL,
	tenant_id int4 NOT NULL,
	start_date date NOT NULL,
	end_date date NOT NULL,
	status text DEFAULT 'Active'::text NULL,
	CONSTRAINT lease_pkey PRIMARY KEY (id)
);


-- public.lease foreign keys

ALTER TABLE public.lease ADD CONSTRAINT lease_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.room(id);
ALTER TABLE public.lease ADD CONSTRAINT lease_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenant(id);


-- public.booking definition

-- Drop table

-- DROP TABLE public.booking;

CREATE TABLE public.booking (
	id serial4 NOT NULL,
	room_id int4 NOT NULL,
	tenant_id int4 NOT NULL,
	start_date date NOT NULL,
	end_date date NOT NULL,
	notes text NULL,
	status text DEFAULT 'Pending'::text NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT booking_pkey PRIMARY KEY (id)
);


-- public.booking foreign keys

ALTER TABLE public.booking ADD CONSTRAINT booking_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.room(id);
ALTER TABLE public.booking ADD CONSTRAINT booking_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenant(id);


-- public.availablerooms source

CREATE OR REPLACE VIEW public.availablerooms
AS SELECT id,
    name
   FROM room
  WHERE occupancy_status = 'Available'::text;

-- public.leasereportview source

CREATE OR REPLACE VIEW public.leasereportview
AS SELECT l.id AS lease_id,
    r.id AS room_id,
    r.name AS room_name,
    (t.first_name || ' '::text) || t.last_name AS tenant_name,
    t.id AS tenant_id,
    l.start_date,
    l.end_date,
    l.status,
    l.end_date - l.start_date AS lease_duration,
        CASE
            WHEN l.status = 'Active'::text THEN 1
            ELSE 0
        END AS active_lease_flag
   FROM lease l
     JOIN room r ON l.room_id = r.id
     JOIN tenant t ON l.tenant_id = t.id;

-- public.leaseview source

CREATE OR REPLACE VIEW public.leaseview
AS SELECT l.id AS lease_id,
    r.name AS room_name,
    (t.first_name || ' '::text) || t.last_name AS tenant_name,
    l.start_date,
    l.end_date,
    l.status
   FROM lease l
     JOIN room r ON l.room_id = r.id
     JOIN tenant t ON l.tenant_id = t.id
  ORDER BY l.start_date DESC;

  -- public.paymentreportview source

CREATE OR REPLACE VIEW public.paymentreportview
AS SELECT p.id AS payment_id,
    r.id AS room_id,
    r.name AS room_name,
    t.id AS tenant_id,
    (t.first_name || ' '::text) || t.last_name AS tenant_name,
    p.amount AS amount_paid,
    p.due_date,
    p.date AS payment_date,
    p.payment_status AS status,
        CASE
            WHEN p.payment_status = 'Overdue'::text THEN p.amount
            ELSE 0::numeric
        END AS overdue_amount
   FROM payment p
     JOIN room r ON p.room_id = r.id
     JOIN tenant t ON p.tenant_id = t.id;


-- public.paymentview source

CREATE OR REPLACE VIEW public.paymentview
AS SELECT p.id,
    r.name AS room_name,
    (t.first_name || ' '::text) || t.last_name AS tenant_name,
    p.amount,
    p.date,
    p.due_date,
    p.method,
    p.payment_status,
    p.reference_number,
    p.notes
   FROM payment p
     JOIN room r ON p.room_id = r.id
     JOIN tenant t ON p.tenant_id = t.id
  ORDER BY p.date DESC;     


  -- public.roomdatareport source

CREATE OR REPLACE VIEW public.roomdatareport
AS SELECT id AS room_id,
    name AS room_name,
    type AS room_type,
    rental_price,
    occupancy_status,
    size AS room_size,
    amenities,
    ( SELECT COALESCE(sum(p.amount), 0::numeric) AS "coalesce"
           FROM payment p
          WHERE p.room_id = r.id) AS total_rent_collected,
    ( SELECT count(*) AS count
           FROM lease l
          WHERE l.room_id = r.id AND l.status = 'Active'::text) AS active_lease_count,
    ( SELECT count(*) AS count
           FROM payment p
          WHERE p.room_id = r.id AND p.payment_status = 'Overdue'::text) AS overdue_payments
   FROM room r;


   -- public.roomdetailswithbooking source

CREATE OR REPLACE VIEW public.roomdetailswithbooking
AS SELECT r.id,
    r.name,
    r.type,
    r.rental_price,
    r.payment_frequency,
    r.security_deposit,
    r.grace_period,
    r.occupancy_status,
    (t.first_name || ' '::text) || t.last_name AS tenant_name,
    COALESCE(b.status, r.occupancy_status) AS dynamic_status
   FROM room r
     LEFT JOIN tenant t ON r.tenant_id = t.id
     LEFT JOIN ( SELECT booking.room_id,
            booking.status
           FROM booking
          WHERE booking.status = ANY (ARRAY['Pending'::text, 'Active'::text])) b ON r.id = b.room_id;

-- public.roomfinancialperformanceview source

CREATE OR REPLACE VIEW public.roomfinancialperformanceview
AS SELECT r.id AS room_id,
    r.name,
    r.type,
    r.rental_price,
    COALESCE(sum(p.amount), 0::numeric) AS total_income,
    r.rental_price * count(p.id)::numeric - COALESCE(sum(p.amount), 0::numeric) AS outstanding
   FROM room r
     LEFT JOIN payment p ON r.id = p.room_id
  GROUP BY r.id, r.name, r.type, r.rental_price;


  -- public.roomoccupancyanalysisview source

CREATE OR REPLACE VIEW public.roomoccupancyanalysisview
AS SELECT occupancy_status,
    count(*) AS count
   FROM room
  GROUP BY occupancy_status;



-- public.roomsummaryview source

CREATE OR REPLACE VIEW public.roomsummaryview
AS SELECT id AS room_id,
    name,
    type,
    size,
    rental_price,
    occupancy_status
   FROM room;            

-- public.tenantreportview source

CREATE OR REPLACE VIEW public.tenantreportview
AS SELECT id AS tenant_id,
    (first_name || ' '::text) || last_name AS tenant_name,
    phone AS contact_number,
    email AS email_address,
    ( SELECT count(*) AS count
           FROM lease
          WHERE lease.tenant_id = t.id AND lease.status = 'Active'::text) AS active_leases,
    ( SELECT COALESCE(sum(payment.amount), 0::numeric) AS "coalesce"
           FROM payment
          WHERE payment.tenant_id = t.id AND payment.payment_status = 'Overdue'::text) AS overdue_balance
   FROM tenant t;   


-- public.tenantview source

CREATE OR REPLACE VIEW public.tenantview
AS SELECT id,
    (first_name || ' '::text) || last_name AS name,
    phone,
    email
   FROM tenant;   




   -- DROP FUNCTION public.add_room(text, text, numeric, numeric, text);

CREATE OR REPLACE FUNCTION public.add_room(room_name text, room_type text, room_size numeric, rental_price numeric, room_amenities text)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
    BEGIN
        INSERT INTO Room (name, type, size, rental_price, amenities)
        VALUES (room_name, room_type, room_size, rental_price, room_amenities);
    END;
    $function$
;



-- DROP FUNCTION public.add_tenant(text, text, text, text);

CREATE OR REPLACE FUNCTION public.add_tenant(first_name text, last_name text, phone text, email text)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN
    INSERT INTO Tenant (first_name, last_name, phone, email)
    VALUES (first_name, last_name, phone, email);
END;
$function$
;



-- DROP FUNCTION public.cancel_lease(int4);

CREATE OR REPLACE FUNCTION public.cancel_lease(lease_id_param integer)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN
    -- Update the lease status to 'Canceled'
    UPDATE Lease
    SET status = 'Canceled'
    WHERE id = lease_id_param;

    -- Update the associated room's occupancy status to 'Available'
    UPDATE Room
    SET occupancy_status = 'Available'
    WHERE id = (SELECT room_id FROM Lease WHERE id = lease_id_param);
END;
$function$
;




-- DROP FUNCTION public.create_lease(int4, int4, date, date);

CREATE OR REPLACE FUNCTION public.create_lease(room_id_param integer, tenant_id_param integer, start_date_param date, end_date_param date)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN
    -- Check for overlapping leases
    IF EXISTS (
        SELECT 1
        FROM Lease l
        WHERE l.room_id = room_id_param  -- Use parameter explicitly
        AND l.status = 'Active'
        AND (
            start_date_param BETWEEN l.start_date AND l.end_date
            OR end_date_param BETWEEN l.start_date AND l.end_date
        )
    ) THEN
        RAISE EXCEPTION 'This room already has an active lease in the selected period.';
    END IF;

    -- Insert lease and update room status
    INSERT INTO Lease (room_id, tenant_id, start_date, end_date, status)
    VALUES (room_id_param, tenant_id_param, start_date_param, end_date_param, 'Active');

    UPDATE Room
    SET occupancy_status = 'Rented'
    WHERE id = room_id_param;
END;
$function$
;



-- DROP FUNCTION public.create_payment(int4, int4, numeric, date, date, text, text, text);

CREATE OR REPLACE FUNCTION public.create_payment(tenant_id integer, room_id integer, amount numeric, payment_date date, due_date date, method text, reference text, notes text)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
    BEGIN
        INSERT INTO Payment (tenant_id, room_id, amount, date, due_date, method, reference_number, notes, payment_status)
        VALUES (tenant_id, room_id, amount, payment_date, due_date, method, reference, notes, 'Paid');

        UPDATE Room
        SET total_rent_collected = total_rent_collected + amount
        WHERE id = room_id;
    END;
    $function$
;


-- DROP FUNCTION public.delete_payment(int4);

CREATE OR REPLACE FUNCTION public.delete_payment(payment_id integer)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
DECLARE
    room_id INTEGER;
    original_amount NUMERIC;
BEGIN
    -- Fetch the original payment amount and associated room_id
    SELECT p.room_id, p.amount
    INTO room_id, original_amount
    FROM Payment p
    WHERE p.id = payment_id;

    -- Check if the payment ID exists
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Payment ID % does not exist', payment_id;
    END IF;

    -- Delete the payment record
    DELETE FROM Payment
    WHERE id = payment_id;

    -- Adjust the room's total rent collected
    UPDATE Room
    SET total_rent_collected = COALESCE(total_rent_collected, 0) - original_amount
    WHERE id = room_id;

END;
$function$
;


-- DROP FUNCTION public.delete_room(int4);

CREATE OR REPLACE FUNCTION public.delete_room(room_id integer)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
    BEGIN
        DELETE FROM Room WHERE id = room_id;
    END;
    $function$
;



-- DROP FUNCTION public.delete_tenant(int4);

CREATE OR REPLACE FUNCTION public.delete_tenant(tenant_id integer)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
    BEGIN
        DELETE FROM Tenant WHERE id = tenant_id;
    END;
    $function$
;
-- DROP FUNCTION public.fetch_available_rooms();

CREATE OR REPLACE FUNCTION public.fetch_available_rooms()
 RETURNS TABLE(id integer, name text)
 LANGUAGE plpgsql
AS $function$
    BEGIN
        RETURN QUERY
        SELECT id, name
        FROM Room
        WHERE occupancy_status = 'Available';
    END;
    $function$
;

-- DROP FUNCTION public.update_lease(int4, date, date, text);

CREATE OR REPLACE FUNCTION public.update_lease(lease_id_param integer, start_date_param date, end_date_param date, status_param text)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN
    -- Update lease details
    UPDATE Lease
    SET start_date = start_date_param,
        end_date = end_date_param,
        status = status_param
    WHERE id = lease_id_param;

    -- Handle automatic updates for room status
    IF status_param = 'Completed' THEN
        UPDATE Room
        SET occupancy_status = 'Available'
        WHERE id = (SELECT room_id FROM Lease WHERE id = lease_id_param);

    ELSIF status_param = 'Canceled' THEN
        UPDATE Room
        SET occupancy_status = 'Available'
        WHERE id = (SELECT room_id FROM Lease WHERE id = lease_id_param);

    ELSIF status_param = 'Active' THEN
        UPDATE Room
        SET occupancy_status = 'Rented'
        WHERE id = (SELECT room_id FROM Lease WHERE id = lease_id_param);
    END IF;
END;
$function$
;

-- DROP FUNCTION public.update_payment(int4, numeric, date, date, text, text, text, text);

CREATE OR REPLACE FUNCTION public.update_payment(payment_id integer, amount_param numeric, payment_date date, due_date_param date, method_param text, reference_param text, notes_param text, status_param text)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
DECLARE
    room_id INTEGER;
    original_amount NUMERIC;
BEGIN
    -- Fetch the original payment amount and associated room_id
    SELECT p.room_id, p.amount
    INTO room_id, original_amount
    FROM Payment p
    WHERE p.id = payment_id;

    -- Check if the payment ID exists
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Payment ID % does not exist', payment_id;
    END IF;

    -- Update payment details
    UPDATE Payment
    SET amount = amount_param,
        date = payment_date,
        due_date = due_date_param,
        method = method_param,
        reference_number = reference_param,
        notes = notes_param,
        payment_status = status_param
    WHERE id = payment_id;

    -- Adjust the room's total rent collected
    UPDATE Room
    SET total_rent_collected = COALESCE(total_rent_collected, 0) - original_amount + amount_param
    WHERE id = room_id;

END;
$function$
;

-- DROP FUNCTION public.update_room(int4, text, text, numeric, numeric, text, text);

CREATE OR REPLACE FUNCTION public.update_room(p_room_id integer, p_room_name text, p_room_type text, p_room_size numeric, p_rental_price numeric, p_room_amenities text, p_occupancy_status text)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN
    UPDATE Room
    SET name = p_room_name,
        type = p_room_type,
        size = p_room_size,
        rental_price = p_rental_price,
        amenities = p_room_amenities,
        occupancy_status = p_occupancy_status
    WHERE id = p_room_id;
END;
$function$
;

-- DROP FUNCTION public.update_tenant(int4, text, text, text, text);

CREATE OR REPLACE FUNCTION public.update_tenant(tenant_id integer, new_first_name text, new_last_name text, new_phone text, new_email text)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
    BEGIN
        UPDATE Tenant
        SET first_name = new_first_name,
            last_name = new_last_name,
            phone = new_phone,
            email = new_email
        WHERE id = tenant_id;
    END;
    $function$
;











