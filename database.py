import sqlite3


conn = sqlite3.connect('example.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE packet_type
             (id INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT
              checksum TEXT, 
              type TEXT, 
              timedate INTEGER, 
              )
             CREATE TABLE sensor_data
             (packet_type_id INTEGER,
              order INTEGER,
              value INTEGER
              FOREIGN KEY(packet_type_id) REFERENCES packet_type(id)''')


# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
