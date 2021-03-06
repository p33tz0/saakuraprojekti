import datetime

import psycopg2
from tabulate import tabulate

from config import config
from weather import req

# This asks for some parameters from user which is used for database.
name = str(input("Anna nimesi: "))

# This asks user for end and start date in YYYY-MM-DD
while True:
    try:
        start = datetime.datetime.strptime(
            input("Anna aloituspäivä YYYY-MM-DD formaatissa: "), "%Y-%m-%d"
        )
        end = datetime.datetime.strptime(
            input("Anna lopetuspäivä YYYY-MM-DD formaatissa: "), "%Y-%m-%d"
        )
        if end < start:
            print("Lopetusaika on aikaisempi kuin aloitusaika")
            continue
        break
    except:
        print("Anna oikeassa formaatissa ")


# This takes the starting time in HHMM format, eg. 0820
while True:
    try:
        a = datetime.datetime.strptime(
            input("Anna aloitusaika HHMM formaatissa: "), "%H%M"
        ).time()
        starttime = a.strftime("%H:%M")
        break
    except:
        print("Anna oikea aika HHMM formaatissa")

# This takes the ending time in HHMM format, eg. 0820
while True:
    try:
        x = datetime.datetime.strptime(
            input("Anna lopetusaika HHMM formaatissa: "), "%H%M"
        ).time()
        endtime = x.strftime("%H:%M")
        break
    except:
        print("Anna oikea aika HHMM formaatissa")

# This combines the end datetime and x datetime.time to a datetime object
enddatetime = datetime.datetime.combine(end, x)
# This combines the start datetime and a datetime.time to a datetime object
startdatetime = datetime.datetime.combine(start, a)


project = str(input("Anna projektin nimi: "))
desc = str(input("Anna projektin selitys: "))

# Here we get the weather description and temperature from openweathermap

weather = req.json()
for i in weather["weather"]:
    weatherdesc = i["description"]
weathertemp = f"{weather['main']['temp']} Celsius"

# Here we create list inside a list for tabulating
paramlist = []
listinner = [name, startdatetime, enddatetime, project, desc, weatherdesc, weathertemp]
paramlist.append(listinner)
headerit = [
    "Name",
    "Start time",
    "Stop time",
    "Project",
    "Project description",
    "Weather",
    "Temperature",
]
testi = tabulate(paramlist, headers=headerit, tablefmt="pretty")
print(testi)


# This is the connection to the database
def connect():
    """Connect to the PostgreSQL database server"""
    con = psycopg2.connect(**config())
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print("Connecting to the PostgreSQL database...")
        con = psycopg2.connect(**params)
        # create a cursor
        cur = con.cursor()
        insert(
            name,
            startdatetime,
            enddatetime,
            project,
            desc,
            weatherdesc,
            weathertemp,
            cur,
        )
        con.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()
            print("Database connection closed.")


# SQL table insert
def insert(
    name, startdatetime, enddatetime, project, desc, weatherdesc, weathertemp, cur
):
    SQL = "INSERT INTO public.saakurataulu (name, startdate, enddate, project, description,\
    weatherdescription, weathertemp) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    cur.execute(
        SQL,
        (
            name,
            startdatetime,
            enddatetime,
            project,
            desc,
            weatherdesc,
            weathertemp,
        ),
    )


# Here we ask if the user wants to send the information to the database or not
while True:
    sendques = str(input("Haluatko lähettää tiedot? Y/N "))
    if sendques.lower() == "y":
        connect()
        break
    else:
        break
