import smtplib
from email.message import EmailMessage


from_addr = input('Your email: ')
passw = input('Your email password: ')
rec_addr = input('Enter receiver email: ')
type = input('Text or html: ')
subj = input('Enter subject: ')
body = input('Enter message text: ')

msg = EmailMessage()
msg['From'] = from_addr
msg['To'] = rec_addr
msg['Subject'] = subj

if type == 'text':
    msg.set_content(body)
else:
    msg.add_alternative("""\
    <!DOCTYPE html>
    <html>
        <body>
            <p style="color:SlateGray;">{text}</p>
        </body>
    </html>
    """.format(text=body), subtype='html')

smtp = smtplib.SMTP_SSL('smtp.mail.ru', 465)
smtp.login(from_addr, passw)
smtp.send_message(msg)
