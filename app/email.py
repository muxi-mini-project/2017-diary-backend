#电子邮件支持

from flask_mail import Message 

def send_email(to,subject,template,**kwargs) :
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject ,
                    sender=app.config['FLASKY_MAIL_SENDER'] ,recipients=[to])
    msg.body = render_template( , **kwargs)
    msg.html =                              # 如何渲染不知道啊啊, 待定
    mail.send(msg) 

