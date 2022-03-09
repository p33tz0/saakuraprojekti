import smtplib
import psycopg2
from config import config
import requests

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("userlogin", "userpassword")
    con = psycopg2.connect(**config())

    try:
        params = config()
        con = psycopg2.connect(**params)
        cur = con.cursor()
        SQL = 'SELECT name, startdate FROM public.saakuraprojekti'
        cur.execute(SQL)
        row = cur.fetchone()
        con.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()
    
    joined_string = " ".join(row)
    content = joined_string
    subject = "Daily report"
    print(joined_string)

    server.sendmail("a@a.com", "a@a.com", f"Subject: {subject}\n{content}")