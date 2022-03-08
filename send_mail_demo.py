import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)

server.ehlo()
server.starttls()
server.ehlo()

server.login("user", "pass")

msg = "\nHello!"
server.sendmail("a@a.com", "a@a.com", msg)