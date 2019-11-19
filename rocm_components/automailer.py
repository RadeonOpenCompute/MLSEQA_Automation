import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os, re

def Auto_mail(htmlfile, subject, textpath):

    fromaddr = "Roccqe.Automailer@amd.com"
    #path= "/home/taccuser/hip_automation/mail/"

    msg = MIMEMultipart()
    msg['From'] = "Roccqe.Automailer@amd.com"
    msg['To'] = "Rahulgoud.Mula@amd.com"
    msg['Cc'] = 'Rahulgoud.Mula@amd.com'
    msg['Subject'] = "%s Unit Test Results"%subject
    body = """<html>
    <head>
    <style>
    table, th, td {
              border: 1px solid black;
                border-collapse: collapse;
                }
    th, td {
              padding: 5px;
                text-align: left;
                }
    </style>
    </head>
    """
 
    try:
        with open(htmlfile, 'r') as readfile:
            body= body+readfile.read()

            msg.attach(MIMEText(body, 'html'))
           
            filename = re.split("/", textpath)
            filename.reverse()
            attachment = open(textpath,'rb')
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" %filename[0])
            msg.attach(p)
        try:
            s = smtplib.SMTP('torsmtp10.amd.com',25)
            s.starttls()
            s.login('rautomai@amd.com', 'Amd12345') # Please give your Password and NIID@amd.com
        except:
            print("Not able to login to mail")
        text = msg.as_string()
        if len(msg['Cc'])==0:
            toaddr = msg['To'].split(",")
        else:
            toaddr = msg['To'].split(",") + msg['Cc'].split(",")
        print(toaddr)
        s.sendmail(msg['From'], toaddr, text)
        s.quit()
        print("Mail sent Successfully\n")

    except smtplib.SMTPServerDisconnected:
        print("server unexpectedly disconnects or SMTP instance before connecting it to a server.")

    except smtplib.SMTPResponseException:
        print("These exceptions are generated in some instances when the SMTP server returns an error code.")

    except smtplib.SMTPSenderRefused:
        print("Sender address refused by SMTP server refused.\nPlease check Sender mail id")
    except smtplib.SMTPConnectError:
        print("Error occurred during establishment of a connection with the server.")
    except IOError:
        print("File not fond\n")
