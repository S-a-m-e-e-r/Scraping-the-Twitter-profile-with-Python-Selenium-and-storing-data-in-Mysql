import mysql.connector

# Create a connection to MySQL
conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="twitterprofiles"
)



# Create a cursor
cursor = conn.cursor()

#Database creation
#curser.execute("CREATE DATABASE twitterprofiles")

# Define the SQL statement to create a table
create_table_query ="""
CREATE TABLE IF NOT EXISTS twitter_profiles1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Bio VARCHAR(1000),
    Following_Count BIGINT,
    Followers_Count BIGINT,
    Location VARCHAR(255),
    Website VARCHAR(255)
)
"""

# Execute the SQL statement
cursor.execute(create_table_query)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Table created successfully!")