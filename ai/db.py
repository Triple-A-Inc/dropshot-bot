from langchain_community.utilities import SQLDatabase

# Define the RDS connection URI
RDS_URI = f"postgresql+psycopg2://{'postgres'}:{'postgres'}@{'dropdb1.c7dhmdz5lx6x.us-east-1.rds.amazonaws.com'}:{5432}/{'dropdb1'}"

# Create the database connection
db = SQLDatabase.from_uri(RDS_URI)

# # Print dialect and usable table names
# print(db.dialect)
# print(db.get_usable_table_names())

# # Run the query and store the result
# query_result = db.run("SELECT * FROM drop_shot_inventory LIMIT 10;")

# # Print the result of the query
# print(query_result)