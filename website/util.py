import smtplib
from email.mime.text import MIMEText
# create email header
from email.header import Header
class Utils:
    # Send email function
    @staticmethod
    def send_mail(to_addr,subject,content):
        from_addr = 'huangvita36@gmail.com' # sender email, change to tutor club email later
        password = 'mqcj qado mmdw jkxa'  # google app password
        smtp_server = 'smtp.gmail.com'

        # Email body, first parameter is email content, second parameter is format, third parameter is encoding
        msg = MIMEText(content, 'plain', 'utf-8')
        # Email header information
        msg['From'] = Header(from_addr)  # sender
        msg['To'] = Header(to_addr)  # receiver
        msg['Subject'] = Header(subject, 'utf-8')  # email subject
        smtpobj = smtplib.SMTP_SSL(smtp_server)
        try:
            # create connection
            smtpobj.connect(smtp_server, 465)
            # login to Google App
            smtpobj.login(from_addr, password)
            # send email
            smtpobj.sendmail(from_addr, to_addr, msg.as_string())
            print("Email sent successfully.")
        except smtplib.SMTPException as e:
            print("Not able to send email.",e)
        finally:
             # close server
            smtpobj.quit()

             #hello