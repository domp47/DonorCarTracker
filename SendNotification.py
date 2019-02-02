import smtplib
import ast
from email.message import EmailMessage

def sendNotification(starkCars, impactCars, copartCars, config):

    msg = EmailMessage()
    msg.set_content(createMessage(starkCars, impactCars, copartCars))

    recipients = ast.literal_eval(config["EMAIL"]["ToAddr"])

    msg["Subject"] = ""
    msg["To"] =  recipients
    msg["From"] = config["EMAIL"]["FromAddr"]

    s = smtplib.SMTP(config["EMAIL"]["SMTP_Server"], config["EMAIL"]["SMTP_Port"])
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(config["EMAIL"]["FromAddr"], config["EMAIL"]["FromPassword"])

    s.sendmail(config["EMAIL"]["FromAddr"], recipients, msg.as_string())
    s.quit()

def createMessage(starkCars, impactCars, copartCars):
    message = ""

    if len(starkCars) > 0:
        message += "New Cars At Stark:\n"

        for car in starkCars:
            message += car.toString()
            message += '\n\n'

    if len(impactCars) > 0:
        if len(starkCars) > 0:
            message += '\n\n'

        message += "New Cars At Impact:\n"

        for car in impactCars:
            message += car.toString()
            message += '\n\n'

    if len(copartCars) > 0:
        if len(impactCars) > 0:
            message += '\n\n'

        message += "New Cars At Copart:\n"

        for car in copartCars:
            message += car.toString()
            message += '\n\n'

    return message
        