import os
import psycopg
from dotenv import load_dotenv
from datetime import datetime

READ_QUERY = """
SELECT ts, value
FROM observations
WHERE series = %s AND ts >= %s AND ts < %s
ORDER BY ts;
"""

def get_series(series:str, date_a:datetime, date_b:datetime):
    args = [series, date_a, date_b]
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(READ_QUERY,args)
            results = cur.fetchall()
            return results
        

def get_connection() -> psycopg.Connection:

    load_dotenv()
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
    connection = psycopg.connect(host="localhost", 
                                 user="elec", 
                                 dbname="elec", 
                                 password=POSTGRES_PASSWORD, 
                                 port=5432)
    
    return connection