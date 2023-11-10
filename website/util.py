import re
import smtplib
from email.mime.text import MIMEText
# 构建邮件头
from email.header import Header
class  Utils:
    # 发送邮件函数
    @staticmethod
    def send_mail(to_addr,subject,contant):
        # 发信方的信息：发信邮箱，QQ 邮箱授权码
        from_addr = 'huangvita36@gmail.com'  # 发送者的邮箱  您的qq邮箱
        password = 'mqcj qado mmdw jkxa'  # 刚才短信获取到的授权码
        # 收信方邮箱
        #to_addr = '********@163.com'
        # 发信服务器
        smtp_server = 'smtp.gmail.com'
        # hello

        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        msg = MIMEText(contant, 'plain', 'utf-8')
        # 邮件头信息
        msg['From'] = Header(from_addr)  # 发送者
        msg['To'] = Header(to_addr)  # 接收者
        #subject = 'Python SMTP 邮件测试'  # 主题
        msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题
        smtpobj = smtplib.SMTP_SSL(smtp_server)  # 创建对象
        try:
            # 建立连接--qq邮箱服务和端口号（可百度查询）
            smtpobj.connect(smtp_server, 465)
            # 登录--发送者账号和口令
            smtpobj.login(from_addr, password)
            # 发送邮件
            smtpobj.sendmail(from_addr, to_addr, msg.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print("无法发送邮件",e)
        finally:
             # 关闭服务器
            smtpobj.quit()



