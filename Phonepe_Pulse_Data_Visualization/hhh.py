import csv
import mysql.connector

# Database connection details
db_host = '127.0.0.1'
db_user = 'root'
db_password = '1234'
db_name = 'phonepe_pulse'
h = '3307'

# CSV file path
csv_file_path = 'C:/Users/samue/Downloads/bus attrocates/Phonepe_Pulse_Data_Visualization-main/Phonepe_Pulse_Data_Visualization-main/Data/top_trans.csv'

# Specify the target table name in your database
table_name = 'top_trans'

# Establish database connection
conn = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name, port=h)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Read CSV file and insert data into the database
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)  # Read the header to get column names

    # Create the SQL query with placeholders for column names
    columns = ', '.join(header)
    placeholders = ', '.join(['%s'] * len(header))
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    # Loop through the rows in the CSV and execute the insert query
    for row in csv_reader:
        cursor.execute(insert_query, row)

# Commit the changes to the database
conn.commit()

# Close the cursor and the database connection
cursor.close()
conn.close()
