import psycopg2

# Replace these values with your RDS instance details
host = 'dropdb1.c7dhmdz5lx6x.us-east-1.rds.amazonaws.com'
port = 5432
database = 'dropdb1'  # Replace with your actual database name
user = 'postgres'
password = 'postgres'

def query_table():
    connection = None
    cursor = None
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        cursor = connection.cursor()

        # SQL query to fetch all data from the table
        cursor.execute("""SELECT *
FROM drop_shot_inventory
WHERE preco > 1000 LIMIT 5;""")
        
        # Fetch all rows from the executed query
        rows = cursor.fetchall()
        
        # Print the rows
        for row in rows:
            print(row)

    except Exception as error:
        print(f"Error while querying the table: {error}")

    finally:
        # Close the cursor and connection to the database if they were initialized
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    query_table()