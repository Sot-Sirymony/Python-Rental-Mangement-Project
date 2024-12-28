import sqlite3
import csv

def get_rent_collection_report():
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT 
        (SELECT first_name || ' ' || last_name FROM Tenant WHERE id = p.tenant_id) AS tenant,
        (SELECT name FROM Room WHERE id = l.room_id) AS room,
        p.amount, p.date,
        CASE WHEN p.amount >= r.rental_price THEN 'Completed' ELSE 'Pending' END AS payment_status
    FROM Payment p
    JOIN Lease l ON p.lease_id = l.id
    JOIN Room r ON l.room_id = r.id
    """)
    data = cursor.fetchall()
    connection.close()
    return data

def get_occupancy_rates():
    connection = sqlite3.connect('rental_management_v2.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT 
        p.name AS property_name,
        r.type AS room_type,
        SUM(CASE WHEN l.start_date <= DATE('now') AND l.end_date >= DATE('now') THEN 1 ELSE 0 END) AS rented_days,
        30 AS available_days,  -- Replace with appropriate logic
        (SUM(CASE WHEN l.start_date <= DATE('now') AND l.end_date >= DATE('now') THEN 1 ELSE 0 END) * 100.0 / 30) AS occupancy_rate
    FROM Room r
    JOIN Property p ON r.property_id = p.id
    LEFT JOIN Lease l ON r.id = l.room_id
    GROUP BY p.name, r.type
    """)
    data = cursor.fetchall()
    connection.close()
    return data

def export_to_csv(report_type):
    data = []
    if report_type == "Rent Collection Report":
        data = get_rent_collection_report()
    elif report_type == "Occupancy Rates":
        data = get_occupancy_rates()
    
    filename = f"{report_type.replace(' ', '_').lower()}.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"Report exported to {filename}")
