import psycopg2
import time


connected = False
while not connected:
    try:
        conn = psycopg2.connect("host=database dbname=postgres user=postgres")
        conn.close();
        print ("Connection to Postgres succeed!")
        connected = True
    except psycopg2.OperationalError:
        print("Unable to connect to Postgres. Retrying...")
        time.sleep(1)
