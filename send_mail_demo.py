#!/usr/bin/python3

import yagmail
import psycopg2
from config import config
import requests
from tabulate import tabulate

def send_mail():
    #DB Connection
    con = psycopg2.connect(**config())

    try:
        params = config()
        con = psycopg2.connect(**params)
        cur = con.cursor()
        #SQL queries are here
        lasku = "UPDATE saakurataulu SET totalminutes=(DATE_PART('day', enddate::timestamp - startdate::timestamp) * 24 + DATE_PART('hour', enddate::timestamp - startdate::timestamp)) * 60 + DATE_PART('minute', enddate::timestamp - startdate::timestamp);"
        lasku2 = "UPDATE saakurataulu SET hoursdecimal = totalminutes / 60;"
        SQL = 'SELECT name as Nimi, startdate, enddate, project, description, weatherdescription, weathertemp, ROUND (hoursdecimal, 2) FROM public.saakurataulu'
        #SQL executions here
        cur.execute(lasku)
        cur.execute(lasku2)
        cur.execute(SQL)
        con.commit()
        #Fetch single row for appending
        row = cur.fetchone()
        lista = []
        #Appending entries from DB to a list inside a list for tabulating later
        while row is not None:
            indexi = 0
            listasis = []
            for i in row:
                jorma = f"{i}"
                listasis.append(jorma)            
                indexi += 1
            lista.append(listasis)
            row = cur.fetchone()
        headerit = ["Name","Start time", "Stop time", "Project", "Project description", "Weather", "Temperature", "Hours"]
            
        #Tabulate results from DB queries to a pretty table
        printti = tabulate(lista, headers=headerit, tablefmt="pretty")
        #Write results from tabulate to a text file 
        with open ("tunnit.txt", "w") as tunnit:
            tunnit.write(printti)
        con.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

    #yag = yagmail.SMTP('userlogin', 'userpassword')
    #subject = "DAILY REPORT"
    #contents = [
    #row
    #]
    
    #yag.send('a@a.com', subject, contents)
   # print("mail sent!")
send_mail()

