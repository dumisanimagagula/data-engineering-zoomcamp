"""Query to find the pickup day with the longest trip distance."""

import psycopg2
import pandas as pd
from datetime import datetime

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="ny_taxi",
    user="root",
    password="root",
    port=5432
)

cursor = conn.cursor()

# Query to find pickup day with longest trip distance (< 100 miles)
query = """
SELECT 
    DATE(tpep_pickup_datetime) as pickup_day,
    MAX(trip_distance) as max_trip_distance,
    COUNT(*) as num_trips
FROM yellow_trip_data
WHERE trip_distance < 100
    AND trip_distance > 0
GROUP BY DATE(tpep_pickup_datetime)
ORDER BY max_trip_distance DESC
LIMIT 10;
"""

print("Querying database for pickup day with longest trip distance (< 100 miles)...\n")

cursor.execute(query)
results = cursor.fetchall()

# Get column names
col_names = [desc[0] for desc in cursor.description]

# Display results
print(f"{'Pickup Day':<15} {'Max Trip Distance':<20} {'Number of Trips':<15}")
print("-" * 50)

if results:
    for row in results:
        pickup_day = row[0]
        max_distance = row[1]
        num_trips = row[2]
        print(f"{str(pickup_day):<15} {max_distance:<20.2f} {num_trips:<15}")
    
    print("\n" + "=" * 50)
    print(f"\nAnswer: The pickup day with the longest trip distance is {results[0][0]}")
    print(f"        with a trip distance of {results[0][1]:.2f} miles")
else:
    print("No results found")

cursor.close()
conn.close()
