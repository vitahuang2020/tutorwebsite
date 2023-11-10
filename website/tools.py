from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'huangvita36@gmail.com'
app.config['MAIL_PASSWORD'] = 'mqcj qado mmdw jkxa'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
class Tools:
    @staticmethod
    def send_message(receive_mail, subject, body):
        msg = Message('Hello', sender='huangvita36@gmail.com', recipients=['huangvita36@gmail.com'])
        msg.body = 'Hello'
        mail.send(msg)
        return True