#!/usr/bin/python3

import yagmail
import psycopg2
from config import config
import requests

def send_mail():

    con = psycopg2.connect(**config())

    try:
        params = config()
        con = psycopg2.connect(**params)
        cur = con.cursor()
        lasku = "UPDATE saakurataulu SET totalminutes=(DATE_PART('day', enddate::timestamp - startdate::timestamp) * 24 + DATE_PART('hour', enddate::timestamp - startdate::timestamp)) * 60 + DATE_PART('minute', enddate::timestamp - startdate::timestamp);"
        SQL = 'SELECT name, startdate, enddate, project, description, weatherdescription, weathertemp, totalminutes FROM public.saakurataulu'
        cur.execute(lasku)
        cur.execute(SQL)
        con.commit()
        colnames = [desc[0] for desc in cur.description]
        print(colnames)
        row = cur.fetchone()
        while row is not None:
            indexi = 0
            for i in row:
                print(f"{i}  {colnames[indexi]}")
                indexi += 1
            row = cur.fetchone()

        
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

