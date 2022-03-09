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
        SQL = 'SELECT name, startdate, enddate, starttime, endtime, weathertemp, weatherdescription FROM public.saakuraprojekti'
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
    print(joined_string)


    yag = yagmail.SMTP('userlogin', 'userpassword')
    
    contents = [
    joined_string
    ]
    yag.send('a@a.com', 'Daily report', contents)
    print("mail sent!")
    

send_mail()

#name, startdate, starttime, enddate, endtime, project, desc, weatherdescription, weathertemp,