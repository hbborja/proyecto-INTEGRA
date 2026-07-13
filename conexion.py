import oracledb
DB_USER = "system"
DB_PASSWORD = "potosi1988"
DB_DSN = "localhost:1521/XE"
def get_db_connection():
    try:
       
        return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
    except oracledb.DatabaseError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None