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

#sql query to select values from table
query="SELECT * FROM twitter_profiles"

# Execute the SQL statement
cursor.execute(query)

#fetching rows
rows=cursor.fetchall()

#labels of the table
labels=["id","Bio", "Following_Count", "Followers_Count", "Location", "Website"]

#iterating through the rows
for r in range(len(rows)):
    ar=rows[r]
    print("-------row:",r+1)
    #iterating through the row values i.e set of row values
    for i in range(len(ar)):
        print(labels[i],":\t",ar[i])
    print(" ")

# Close the cursor and connection
cursor.close()
conn.close()

