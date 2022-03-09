#!/usr/bin/python3

import yagmail
import psycopg2
from config import config
import requests
from tabulate import tabulate

def send_mail():

    con = psycopg2.connect(**config())

    try:
        params = config()
        con = psycopg2.connect(**params)
        cur = con.cursor()
        #lasku = "UPDATE saakurataulu SET totalminutes=(DATE_PART('day', enddate::timestamp - startdate::timestamp) * 24 + DATE_PART('hour', enddate::timestamp - startdate::timestamp)) * 60 + DATE_PART('minute', enddate::timestamp - startdate::timestamp);"
        #lasku2 = "UPDATE saakurataulu SET hoursdecimal = totalminutes / 60;"
        SQL = 'SELECT name as Nimi, startdate, enddate, project, description, weatherdescription, weathertemp FROM public.saakurataulu'
        #cur.execute(lasku)
        #cur.execute(lasku2)
        cur.execute(SQL)
        con.commit()
        colnames = [desc[0] for desc in cur.description]
        print(colnames)
        row = cur.fetchone()
        lista = []
        listauusi = {}
        #dicts = {}
        while row is not None:
            indexi = 0
            ind = 0
            listasis = []
            for i in row:
                jorma = f"{i}"
                listasis.append(jorma)


                
                indexi += 1
            lista.append(listasis)
            row = cur.fetchone()
        headerit = ["Nimi","Aloitusaika", "Lopetusaika", "Projekti", "Projektikuvaus", "Sää", "Lämpötila"]
        print(tabulate(lista, headers=headerit, tablefmt="pretty"))
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

