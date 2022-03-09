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
        SQL = 'SELECT name, startdate, enddate, project, description, weatherdescription, weathertemp, totalhours FROM public.saakuraprojekti'
        cur.execute(SQL)
        row = cur.fetchall()
        con.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

    yag = yagmail.SMTP('userlogin', 'userpassword')
    subject = "DAILY REPORT"
    contents = [
    row
    ]
    
    yag.send('a@a.com', subject, contents)
    print("mail sent!")
    

send_mail()
    
    joined_string = " ".join(row)
    content = joined_string
    subject = "Daily report"
    print(joined_string)

    server.sendmail("a@a.com", "a@a.com", f"Subject: {subject}\n{content}")
