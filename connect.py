import psycopg2
from config import config

def connect():
    """ Connect to the PostgreSQL database server """
    con = psycopg2.connect(**config())
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        con = psycopg2.connect(**params)
		
        # create a cursor
        cur = con.cursor()
        #insert(cur)
        #deleteperson(6, cur)
        select_all(cur)
        con.commit()

        # print('PostgreSQL database version:')
        # cur.execute('SELECT version()')

        # db_version = cur.fetchone()
        # print(db_version)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()
            print('Database connection closed.')

def select_all(cur):
    SQL = 'SELECT * FROM person'
    cur.execute(SQL)
    colnames = [desc[0] for desc in cur.description]
    print(colnames)
    row = cur.fetchone()
    while row is not None:
        print(row)
        row = cur.fetchone()

def insert(cur):
    SQL = "INSERT INTO person (name, age) VALUES ('Pasi', 22);"
    cur.execute(SQL)

def deleteperson(id, cur):
    SQL = "DELETE FROM person WHERE id = %s;"
    data = (id,)
    cur.execute(SQL, data)

connect()