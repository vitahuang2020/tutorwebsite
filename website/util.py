import smtplib
from email.mime.text import MIMEText
# create email header
from email.header import Header
class Utils:
    # Send email function
    # @staticmethod
    # def send_mail(to_addr,subject,content):
    #     from_addr = 'huangvita36@gmail.com' # sender email, change to tutor club email later
    #     password = 'mqcj qado mmdw jkxa'  # google app password
    #     smtp_server = 'smtp.gmail.com'
    #
    #     # Email body, first parameter is email content, second parameter is format, third parameter is encoding
    #     msg = MIMEText(content, 'plain', 'utf-8')
    #     # Email header information
    #     msg['From'] = Header(from_addr)  # sender
    #     msg['To'] = Header(to_addr)  # receiver
    #     msg['Subject'] = Header(subject, 'utf-8')  # email subject
    #     smtpobj = smtplib.SMTP_SSL(smtp_server)
    #     try:
    #         # create connection
    #         smtpobj.connect(smtp_server, 465)
    #         # login to Google App
    #         smtpobj.login(from_addr, password)
    #         # send email
    #         smtpobj.sendmail(from_addr, to_addr, msg.as_string())
    #         print("Email sent successfully.")
    #     except smtplib.SMTPException as e:
    #         print("Not able to send email.",e)
    #     finally:
    #          # close server
    #         smtpobj.quit()
    #
    #          #hello

    @staticmethod
    def send_mail(to_addr, subject, content):
        # 设置邮件内容
        from_addr = 'gotime_wxb@163.com'
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = Header(from_addr)
        message['To'] = Header(to_addr)
        message['Subject'] = Header(subject)
        # 发送邮件
        try:
            smtp_obj = smtplib.SMTP_SSL('smtp.163.com', 465)  # 设置smtp服务器地址
            smtp_obj.login(from_addr, 'EYDOFQPOCUOSTJCV')  # 登录smtp服务器
            smtp_obj.sendmail(from_addr, [to_addr], message.as_string())  # 发送邮件
            smtp_obj.quit()
            print("邮件发送成功")
            return True;
        except Exception as e:
            print(f"邮件发送失败{e}")
            return False;