import psycopg2
import datetime
from config import config
import requests
from weather import req

#This asks for some parameters from user which is used for database.
name = str(input("Anna nimesi: "))

#This asks for year, month and day for the starting date
def startdate():
    startdateyear = int(input("Aloitusaika: Anna vuosi: "))
    startdatemonth = int(input("Aloitusaika: Anna kuukauden numero: "))
    startdateday = int(input("Aloitusaika: Anna päivän numero: "))
    #This combines the former to a proper date
    startdate = datetime.date(startdateyear, startdatemonth, startdateday)
    return startdate


#This asks user for end and start date in YYYY-MM-DD
while True:
    try:
        start = datetime.datetime.strptime(input('Anna aloituspäivä YYYY-MM-DD formaatissa: '), '%Y-%m-%d')
        startdate = start.strftime('%Y-%m-%d')
        end = datetime.datetime.strptime(input("Anna lopetuspäivä YYYY-MM-DD formaatissa: "), '%Y-%m-%d')
        enddate = end.strftime('%Y-%m-%d')
        if enddate < startdate:
            print("Lopetusika on aikaisempi kuin aloitusaika")
            continue
        break
    except:
        print("Anna oikeassa formaatissa / ")

#This takes the starting time in HHMM format, eg. 0820
while True:
    try: 
        a = datetime.datetime.strptime(input('Anna aloitusaika HHMM formaatissa: '), "%H%M")
        starttime = a.strftime("%H:%M")
        print(starttime)
        break
    except:
        print("Anna oikea aika HHMM formaatissa")


#This takes the ending time in HHMM format, eg. 0820
while True:
    try: 
        a = datetime.datetime.strptime(input('Anna lopetusaika HHMM formaatissa: '), "%H%M")
        endtime = a.strftime("%H:%M")
        break
    except:
        print("Anna oikea aika HHMM formaatissa")

#
project = str(input("Anna projektin nimI: ")
desc = str(input("Anna projektin selitys: "))

#Here we get the weather description and temperature from openweathermap

weather = req.json()
for i in weather["weather"]:
    weatherdesc = (i['description'])
weathertemp = f"{weather['main']['temp']} Celsius"





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
        insert(cur)
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

def insert(name, startdate, starttime, enddate, endtime, project, desc, weatherdesc, weathertemp cur):
    SQL = "INSERT INTO person (name, startdate, starttime, enddate, endtime, project, description,\
        weatherdescription, weathertemp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    data = (f"{name}", f"{startdate}", f"{starttime}", f"{enddate}", f"{endtime}", f"{project}",\
        f"{desc}", f"{weatherdesc}", f"{weathertemp}")
        
    cur.execute(SQL, data)