import psycopg2
import csv

# Replace these values with your RDS instance details
host = 'dropdb1.c7dhmdz5lx6x.us-east-1.rds.amazonaws.com'
port = 5432
database = 'dropdb1'  # Replace with your actual database name
user = 'postgres'
password = 'postgres'

# Path to your CSV file
csv_file_path = '/Users/beylouni/Downloads/vendasdropestoque - Página2.csv'

# SQL query to insert data into the table
insert_query = """
INSERT INTO drop_shot_inventory (descricao, sku, unidade, preco, estoque_fisico, estoque_disponivel)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (sku) DO NOTHING;  -- This avoids duplication based on the primary key (sku)
"""

def clean_numeric_value(value):
    """Clean numeric values by replacing commas with periods for compatibility with PostgreSQL."""
    try:
        return float(value.replace(',', '.')) if value else None
    except ValueError:
        return None

def insert_data_from_csv(csv_file_path):
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

        # Open the CSV file and read data
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip header row if your CSV has headers

            for row in csv_reader:
                # Clean the numeric fields before inserting them into the database
                row[3] = clean_numeric_value(row[3])  # Clean 'preco'
                row[4] = clean_numeric_value(row[4])  # Clean 'estoque_fisico'
                row[5] = clean_numeric_value(row[5])  # Clean 'estoque_disponivel'

                # Insert each row into the database
                cursor.execute(insert_query, row)

        # Commit the transaction
        connection.commit()

        print(f"Data from '{csv_file_path}' inserted successfully into 'drop_shot_inventory'.")

    except Exception as error:
        print(f"Error while inserting data: {error}")

    finally:
        # Close the cursor and connection to the database if they were initialized
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    insert_data_from_csv(csv_file_path)