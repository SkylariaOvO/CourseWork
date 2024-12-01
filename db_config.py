import psycopg2

#commands entered into db: 
"""
CREATE TABLE UserTbl (
    userID SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL
);
"""


CONNECTION_STRING = "postgresql://neondb_owner:eNHWkd1I3hXF@ep-white-hat-a4px9qng.us-east-1.aws.neon.tech/neondb?sslmode=require"

def get_connection():
    try:
        conn = psycopg2.connect(CONNECTION_STRING)
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

if __name__ == "__main__":
  conn = get_connection()
  if conn:
      print("Connection successful!")
      conn.close()
  else:
      print("Failed to connect to the database.")
