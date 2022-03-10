from crontab import CronTab

cron = CronTab(user=True)
job = cron.new(command='cd / && python3 send_mail.py')
job.minute.every(1)

cron.write()