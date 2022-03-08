import psycopg2
import datetime
from config import config
import requests

#Here we connect to the table in PostgreSQL server 

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
        
    # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()
            print('Database connection closed.')


#This asks for some parameters from user which is used for database.
name = str(input("Anna nimesi: "))
def startdate():
    #This asks for year, month and day for the starting date
    startdateyear = int(input("Aloitusaika: Anna vuosi: "))
    startdatemonth = int(input("Aloitusaika: Anna kuukauden numero: "))
    startdateday = int(input("Aloitusaika: Anna päivän numero: "))
    #This combines the former to a proper date
    startdate = datetime.date(startdateyear, startdatemonth, startdateday)
    return startdate

#This takes the starting time in HHMM format, eg. 0820
try: 
    a = datetime.datetime.strptime(raw_input('Anna aloitusaika HHMM formaatissa: '), "%H%M")
    starttime = a.strftime("%H%M")
except:
    print("Anna oikea aika HHMM formaatissa")

def enddate():
    enddateyear = int(input("Lopetusaika: Anna vuosi:  "))
    enddatemonth = int(input("Lopetusaika: Anna kuukauden numero: "))
    enddateday = int(input("Lopetusika: Anna päivän numeero: "))
    enddate = datetime.date(enddateyear, enddatemonth, enddateday)
    return enddate

project = str(input("Anna projektin nimI: ")
description = str(input("Anna projektin selitys: "))

#Here we get the weather description and temperature from openweathermap
req = requests.get("http://api.openweathermap.org/data/2.5/weather?lat=60.1695&lon=24.9355&appid=6efc1791652387ffbf2eaf2934333384&lang=fi&units=metric")
weather = req.json()
for i in weather["weather"]:
    weatherdesc = (i['description'])
weathertemp = f"{weather['main']['temp']} Celsius"