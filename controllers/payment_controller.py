import sqlite3

def add_payment(tenant, room, amount, date, method):
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO Payment (tenant_id, room_id, amount, date, method)
    VALUES (
        (SELECT id FROM Tenant WHERE first_name || ' ' || last_name = ?),
        (SELECT id FROM Room WHERE name = ?),
        ?, ?, ?
    )
    """, (tenant, room, amount, date, method))
    connection.commit()
    connection.close()

def get_all_payments():
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT 
        (SELECT first_name || ' ' || last_name FROM Tenant WHERE id = p.tenant_id) AS tenant,
        (SELECT name FROM Room WHERE id = p.room_id) AS room,
        p.amount, p.date, p.method 
    FROM Payment p
    """)
    payments = [{"tenant": row[0], "room": row[1], "amount": row[2], "date": row[3], "method": row[4]} for row in cursor.fetchall()]
    connection.close()
    return payments
