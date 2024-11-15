import psycopg2
try:
    conn = psycopg2.connect(
        host="clowncore.c144myww860a.ap-south-1.rds.amazonaws.com",
        port=5432,
        database="postgres",
        user="clowncore",
        password="clowncoreM&a"
    )
    print("Connection successful")
    conn.close()
except Exception as e:
    print("Unable to connect:", e)
