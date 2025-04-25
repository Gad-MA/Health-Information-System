import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables from the .env file
load_dotenv()


DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Connect to PostgresSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# Create a cursor object
cur = conn.cursor()


queries = [
    """
    CREATE TABLE operation_room (
        id SERIAL PRIMARY KEY,
        room_number VARCHAR(10) UNIQUE NOT NULL,
        is_available BOOLEAN DEFAULT TRUE
    );
    """,
    """
    CREATE TABLE his_user (
        id SERIAL PRIMARY KEY,
        username VARCHAR(150) UNIQUE NOT NULL,
        email VARCHAR(254) UNIQUE NOT NULL,
        role VARCHAR(10) CHECK (role IN ('patient', 'surgeon')) NOT NULL
    );
    """,
    """
    CREATE TABLE surgery_case (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER REFERENCES his_user(id),
        surgeon_id INTEGER REFERENCES his_user(id),
        operation_room_id INTEGER REFERENCES operation_room(id),
        date_time TIMESTAMP NOT NULL,
        procedure_type VARCHAR(100),
        status VARCHAR(20) CHECK (status IN ('scheduled', 'in_progress', 'completed')) DEFAULT 'scheduled'
    );
    """,
    """
    CREATE TABLE pre_op_checklist (
        id SERIAL PRIMARY KEY,
        surgery_case_id INTEGER UNIQUE REFERENCES surgery_case(id),
        consent_signed BOOLEAN DEFAULT FALSE,
        allergies_checked BOOLEAN DEFAULT FALSE,
        lab_results_ok BOOLEAN DEFAULT FALSE
    );
    """,
    """
    CREATE TABLE post_op_report (
        id SERIAL PRIMARY KEY,
        surgery_case_id INTEGER UNIQUE REFERENCES surgery_case(id),
        outcome TEXT NOT NULL,
        notes TEXT,
        follow_up_date DATE
    );
    """
]

# Execute
for query in queries:
    try:
        cur.execute(query)
        print("Query executed successfully")
    except Exception as e:
        print(f"Error executing query: {e}")

# Commit changes and close the connection
conn.commit()
cur.close()
conn.close()
