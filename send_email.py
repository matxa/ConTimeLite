""" Send Email """
import smtplib
from email.message import EmailMessage


def email(name, date, files, reciever, hours):
    """ Send Email
    """
    msg = EmailMessage()
    msg['Subject'] = f'{name} -|- Calendar - {date}'
    msg['From'] = 'contimework@gmail.com'
    msg['To'] = reciever
    msg.set_content(f"""<h2>Employee: {name}</h2>\n
    <h3>Total Hours: {hours}</h3>\n
    """ + files[0].read() + """<a href="https://lite.contime.work/">
    \n<br>\n<br>
    Visit ConTimeLite</a>
    """, subtype='html')
    msg.add_attachment(
        files[1].read(), subtype='csv', filename=files[1].name)
    msg.add_attachment(
        files[2].read(), subtype='json', filename=files[2].name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('EMAIL', 'PASSWORD')
        smtp.send_message(msg)
